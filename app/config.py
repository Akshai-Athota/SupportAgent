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
VECTOR_SIZE = int(os.getenv("VECTOR_SIZE"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE"))
BASE_DIR = Path(os.getenv("BASE_DIR"))
CSV_PATH =  Path(os.getenv("CSV_PATH"))
POLICY_PATH =  Path(os.getenv("POLICY_PATH"))
RAG_THRESHOLD=float(os.getenv("RAG_THRESHOLD"))
DOCUMENT_LIMT=int(os.getenv("DOCUMENT_LIMT"))
DATABSE_URL = os.getenv("POSTGRESS_SQL")
REFUND_THRESHOLD=int(os.getenv("REFUND_THRESHOLD"))
MY_API_KEY=os.getenv("MY_API_KEY")
RATE_LIMT=os.getenv("RATE_LIMT")
LOG_LEVEL=os.getenv("LOG_LEVEL")
JWT_SECRET=os.getenv("JWT_SECRET")        
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
MAX_TOKENS_CHECKPOINTER=int(os.getenv("MAX_TOKENS_CHECKPOINTER"))