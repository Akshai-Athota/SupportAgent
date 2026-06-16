from app.schemas.chat_schema import chatRequest,chatResponse
from app.rag.retriver import retriver_documents
from app.agents.llm import llm

from fastapi import APIRouter


chat_route = APIRouter(prefix="/chat",tags=["chat"])

@chat_route.post("")
def get_response_for_query(request:chatRequest)->chatResponse:
    query = request.query

    documents = retriver_documents(query=query)

    if not documents:
        return chatResponse(
            response="Sorry, I couldn't find an answer. I can connect you with a human agent.", 
            source=[], 
            intent=[], 
            category=[]
        )

    try:
        context = "\n\n".join(f"[{d.source}/{d.intent}] {d.response}" for d in documents)
        response = llm.invoke({"knowledge_base": context,"question":query}).content
        
        return chatResponse(
            response=response, 
            source=[doc.source for doc in documents], 
            intent=[doc.intent for doc in documents], 
            category=[doc.category for doc in documents]
        )

    except Exception as e:
        return chatResponse(
            response="Sorry, I couldn't find an answer. I can connect you with a human agent.", 
            source=[], 
            intent=[], 
            category=[]
        )