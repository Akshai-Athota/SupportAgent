import json
from uuid import uuid4
from pathlib import Path


import pandas as pd
from qdrant_client.models import Distance, VectorParams, PointStruct, Document ,SparseVectorParams,Modifier

from app.qdrant_client import client
from app.config import COLLECTION_NAME,EMBEDDING_MODEL,SPARSE_MODEL


VECTOR_SIZE = 384
BATCH_SIZE = 200
BASE_PATH = Path(__file__).resolve().parents[1]
CSV_PATH = BASE_PATH / "data" / "customer_chat_data.csv"
POLICY_PATH = BASE_PATH / "data" / "policy_docs.json"

def build_point(question, response, category, intent, source):
    return PointStruct(
        id=str(uuid4()),
        vector={
            "dense": Document(text=question, model=EMBEDDING_MODEL),
            "sparse": Document(text=question, model=SPARSE_MODEL),   # "Qdrant/bm25"
        },
        payload={"response": response, "category": category, "intent": intent, "source": source},
    )


def load_points():
    points = []

    df = pd.read_csv(Path(CSV_PATH))
    for row in df.itertuples(index=False):
        points.append(build_point(row.instruction, row.response, row.category, row.intent, "faq"))

    with open(Path(POLICY_PATH), encoding="utf-8") as f:
        for doc in json.load(f):
            points.append(build_point(doc["question"], doc["response"], doc["category"], doc["intent"], "policy"))

    return points


def recreate_collection():
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={"dense":VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)},
        sparse_vectors_config={"sparse":SparseVectorParams(modifier=Modifier.IDF)}
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



if __name__ == "__main__":
    main()