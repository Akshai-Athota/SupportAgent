from qdrant_client import models
from app.qdrant_client import client
from app.config import COLLECTION_NAME,EMBEDDING_MODEL,RAG_THRESHOLD,DOCUMENT_LIMT,RERANK_MODEL,CANDIDATE_LIMIT,SPARSE_MODEL
from app.schemas.kb_schema import kbResponse

from qdrant_client.models import Document

from app.agents.reranking import reranker


from qdrant_client import models
from qdrant_client.models import Document

def retriver_documents(query, threshold=RAG_THRESHOLD, limt=DOCUMENT_LIMT):
    hits = client.query_points(
        collection_name=COLLECTION_NAME,
        prefetch=[
            models.Prefetch(query=Document(text=query, model=EMBEDDING_MODEL),
                            using="dense", limit=CANDIDATE_LIMIT),
            models.Prefetch(query=Document(text=query, model=SPARSE_MODEL),
                            using="sparse", limit=CANDIDATE_LIMIT),
        ],
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        limit=CANDIDATE_LIMIT,
    ).points

    if not hits:
        return []

    documents = [hit.payload["response"] for hit in hits]
    reranked = reranker.rerank(model=RERANK_MODEL, query=query, documents=documents, top_n=limt)

    results = []
    for r in reranked.results:
        if r.relevance_score < threshold:
            continue
        hit = hits[r.index]
        results.append(kbResponse(
            response=hit.payload["response"], source=hit.payload["source"],
            intent=hit.payload["intent"], category=hit.payload["category"],
        ))
    return results
