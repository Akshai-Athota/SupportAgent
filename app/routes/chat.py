from app.schemas.chat_schema import chatRequest, chatResponse
from app.agents.react_agent import agent_graph

from langchain_core.messages import HumanMessage
from fastapi import APIRouter

chat_route = APIRouter(prefix="/chat", tags=["chat"])

@chat_route.post("")
def get_response_for_query(request: chatRequest) -> chatResponse:
    query = request.query
    try:
        result = agent_graph.invoke(
            {"messages": [HumanMessage(content=query)], "query": query},
            config={"recursion_limit": 10},
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
        print(f"/chat error: {e}")   
        return chatResponse(
            response="Sorry, I couldn't find an answer. I can connect you with a human agent.",
            tools_used=[],
        )