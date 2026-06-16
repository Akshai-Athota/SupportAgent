from app.config import qdrant_creds
from qdrant_client import QdrantClient

client = QdrantClient(api_key=qdrant_creds.api_key,url=qdrant_creds.url,cloud_inference=True)

