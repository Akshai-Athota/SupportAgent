from app.schemas.chat_schema import chatRequest, chatResponse
from app.agents.react_agent import agent_graph
from app.security.api_key_security import verify_api_key
from app.utils.rate_limit import limiter
from app.config import RATE_LIMT
from app.security.token_verification import get_current_customer
from app.crud.conversation import create_conversation,get_conversation

from langchain_core.messages import HumanMessage
from fastapi import APIRouter,Depends,Request
import logging

logger = logging.getLogger(__name__)


chat_route = APIRouter(prefix="/chat", tags=["chat"])

@chat_route.post("")
@limiter.limit(RATE_LIMT + "/minute")
def get_response_for_query(
    request: Request,
    request_body: chatRequest,
    conversation_id: str | None = None,
    customer_id: int = Depends(get_current_customer),
) -> chatResponse:
    query = request_body.query

    if conversation_id is None:
        conversation_id = create_conversation(customer_id=customer_id,title=None).id
    elif not get_conversation(customer_id=customer_id, conversation_id=conversation_id):
        return chatResponse(response="Sorry, you don't have access to that conversation.",
                            tools_used=[], conversation_id=conversation_id)

    try:
        result = agent_graph.invoke(
            {"messages": [HumanMessage(content=query)], "query": query, "customer_id": customer_id},
            config={"configurable": {"thread_id": conversation_id}, "recursion_limit": 10},
        )
        tools_used = [tc["name"] for m in result["messages"]
                      if getattr(m, "tool_calls", None) for tc in m.tool_calls]
        return chatResponse(response=result["messages"][-1].content,
                            tools_used=tools_used, conversation_id=conversation_id)
    except Exception:
        logger.exception("chat_failed")
        return chatResponse(response="Sorry, I couldn't find an answer. I can connect you with a human agent.",
                            tools_used=[], conversation_id=conversation_id)