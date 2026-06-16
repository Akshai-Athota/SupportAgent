from app.qdrant_client import client
from app.config import COLLECTION_NAME,EMBEDDING_MODEL,RAG_THRESHOLD,DOCUMENT_LIMT
from app.schemas.kb_schema import kbResponse

from qdrant_client.models import Document


def retriver_documents(query:str,threshold:float=RAG_THRESHOLD,limt:int=DOCUMENT_LIMT):
    hits = client.query_points(
        collection_name=COLLECTION_NAME,
        query=Document(
            text = query,
            model=EMBEDDING_MODEL,
        ),
        limit=limt, 
    ).points

    hits = [hit for hit in hits if hit.score >= threshold]

    responses = [
        kbResponse(
            response=hit.payload["response"],
            source=hit.payload["source"],
            intent=hit.payload["intent"],
            category=hit.payload["category"]
        )
        for hit in hits
    ]

    return responses
