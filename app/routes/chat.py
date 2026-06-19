from app.schemas.chat_schema import chatRequest, chatResponse
from app.agents.react_agent import agent_graph
from app.security.api_key_security import verify_api_key
from app.utils.rate_limit import limiter
from app.config import RATE_LIMT

from langchain_core.messages import HumanMessage
from fastapi import APIRouter,Depends,Request
import logging

logger = logging.getLogger(__name__)


chat_route = APIRouter(prefix="/chat", tags=["chat"],dependencies=[Depends(verify_api_key)])

@chat_route.post("")
@limiter.limit(limit_value=RATE_LIMT+"/minute")
def get_response_for_query(request:Request,request_body: chatRequest,thread_id:int=1) -> chatResponse:
    query = request_body.query
    try:
        result = agent_graph.invoke(
            {"messages": [HumanMessage(content=query)], "query": query},
            config={"configurable":{"thread_id":thread_id},"recursion_limit": 10},
        )
        tools_used = [
            tc["name"]
            for message in result["messages"]
            if getattr(message, "tool_calls", None)
            for tc in message.tool_calls
        ]
        return chatResponse(
            response=result["messages"][-1].content,
            tools_used=tools_used,
        )
    except Exception as e:
        logger.exception(f"chat failed with exception: {e}")  
        return chatResponse(
            response="Sorry, I couldn't find an answer. I can connect you with a human agent.",
            tools_used=[],
        )