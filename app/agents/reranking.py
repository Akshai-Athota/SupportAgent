import cohere

from app.config import COHERE_API_KEY

reranker = cohere.ClientV2(api_key=COHERE_API_KEY)