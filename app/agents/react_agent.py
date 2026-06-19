from typing import Annotated, Sequence, Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.messages import (
    BaseMessage, SystemMessage, HumanMessage, AIMessage, ToolMessage,
)

from app.agents.memory.postgres_saver import checkpointer as postgress_checkpointer
from app.agents.prompts.brain_prompt import SYSTEM_PROMPT
from app.tools.tools import tools
from app.agents.llm import model,kb_chain           


model_with_tools = model.bind_tools(tools)



class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    query: str


def brain_node(state: AgentState):
    response = model_with_tools.invoke([SYSTEM_PROMPT] + list(state["messages"]))
    return {"messages": [response]}


def kb_answer_node(state: AgentState):
    kb_content = state["messages"][-1].content          
    answer = kb_chain.invoke({"question": state["query"], "knowledge_base": kb_content})
    return {"messages": [AIMessage(content=answer.content)]}


def should_continue(state: AgentState) -> Literal["tool_node", "__end__"]:
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None):
        return "tool_node"
    return END


def route_after_tools(state: AgentState) -> Literal["kb_answer", "brain"]:
    last = state["messages"][-1]
    if isinstance(last, ToolMessage) and last.name == "search_knowledge_base":
        return "kb_answer"
    return "brain"


graph = StateGraph(AgentState)

graph.add_node("brain", brain_node)
graph.add_node("tool_node", ToolNode(tools))
graph.add_node("kb_answer", kb_answer_node)

graph.add_edge(START, "brain")
graph.add_conditional_edges("brain", should_continue)
graph.add_conditional_edges("tool_node", route_after_tools)
graph.add_edge("kb_answer", END)       

agent_graph = graph.compile(checkpointer=postgress_checkpointer)


if __name__ == "__main__":
    q = "what is the return policy of your company?"
    result = agent_graph.invoke(
        {"messages": [HumanMessage(content=q)], "query": q},
        config={"recursion_limit": 10},
    )
    print(result["messages"])