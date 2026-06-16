import json
from uuid import uuid4

import pandas as pd
from qdrant_client.models import Distance, VectorParams, PointStruct, Document

from app.qdrant_client import client
from app.config import COLLECTION_NAME,EMBEDDING_MODEL,VECTOR_SIZE,BATCH_SIZE,CSV_PATH,POLICY_PATH

def build_point(question, response, category, intent, source):
    return PointStruct(
        id=str(uuid4()),
        vector=Document(text=question, model=EMBEDDING_MODEL),
        payload={"response": response, "category": category, "intent": intent, "source": source},
    )


def load_points():
    points = []

    df = pd.read_csv(CSV_PATH)
    for row in df.itertuples(index=False):
        points.append(build_point(row.instruction, row.response, row.category, row.intent, "faq"))

    with open(POLICY_PATH, encoding="utf-8") as f:
        for doc in json.load(f):
            points.append(build_point(doc["question"], doc["response"], doc["category"], doc["intent"], "policy"))

    return points


def recreate_collection():
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )


def upsert_in_batches(points):
    for i in range(0, len(points), BATCH_SIZE):
        batch = points[i:i + BATCH_SIZE]
        client.upsert(collection_name=COLLECTION_NAME, points=batch)
        print(f"Upserted {min(i + BATCH_SIZE, len(points))}/{len(points)}")


def main():
    recreate_collection()
    points = load_points()
    upsert_in_batches(points)

    count = client.count(collection_name=COLLECTION_NAME).count
    print(f"Done. Collection holds {count} points.")

    hits = client.query_points(
        collection_name=COLLECTION_NAME,
        query=Document(text="How do I get a refund?", model=EMBEDDING_MODEL),
        limit=3,
    ).points
    for h in hits:
        print(round(h.score, 3), h.payload["source"], h.payload["intent"], "->", h.payload["response"][:80])


if __name__ == "__main__":
    main()