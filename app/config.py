from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

class chatModel:
    groq_api_key = os.getenv("GROQ_API_KEY")
    model_name  = os.getenv("MODEL")

class qdrantCreds:
    api_key = os.getenv("QDRANT_API_KEY")
    url = os.getenv("QDRANT_END_POINT")


chat_model = chatModel()
qdrant_creds = qdrantCreds()

COLLECTION_NAME = os.getenv("COLLECTION_NAME")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
RAG_THRESHOLD=float(os.getenv("RAG_THRESHOLD"))
DOCUMENT_LIMT=int(os.getenv("DOCUMENT_LIMT"))
CANDIDATE_LIMIT=int(os.getenv("CANDIDATE_LIMIT"))
DATABSE_URL = os.getenv("POSTGRESS_SQL")
REFUND_THRESHOLD=int(os.getenv("REFUND_THRESHOLD"))
MY_API_KEY=os.getenv("MY_API_KEY")
RATE_LIMT=os.getenv("RATE_LIMT")
LOG_LEVEL=os.getenv("LOG_LEVEL")
JWT_SECRET=os.getenv("JWT_SECRET")        
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
MAX_TOKENS_CHECKPOINTER=int(os.getenv("MAX_TOKENS_CHECKPOINTER"))
COHERE_API_KEY=os.getenv("COHERE_API_KEY")
RERANK_MODEL=os.getenv("RERANK_MODEL")
SPARSE_MODEL=os.getenv("SPARSE_MODEL")