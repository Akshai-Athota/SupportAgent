from typing import Annotated, Sequence, Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.store.base import BaseStore
from langgraph.prebuilt import ToolNode
from langchain_core.messages import (
    BaseMessage, SystemMessage, HumanMessage, AIMessage, ToolMessage,trim_messages
)

from app.agents.memory.postgres_saver import checkpointer as postgress_checkpointer
from app.agents.memory.postgres_store import storepointer as postgress_store
from app.agents.prompts.brain_prompt import SYSTEM_PROMPT
from app.tools.tools import tools
from app.agents.llm import model,kb_chain   
from app.config import MAX_TOKENS_CHECKPOINTER        


model_with_tools = model.bind_tools(tools)



class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    query: str
    customer_id : int
    memories : str

def load_memory_node(state:AgentState,*,store:BaseStore):
    namespace = ("memories",str(state["customer_id"]))
    items = store.search(namespace)
    memories = "\n".join(f"- {item.value['text']}" for item in items)
    return {"memories": memories}


def brain_node(state: AgentState):
    sys = SYSTEM_PROMPT
    if state.get("memories"):
        sys = SystemMessage(content=SYSTEM_PROMPT.content +
                            f"\n\nKnown facts about this customer:\n{state['memories']}")
    trimmed = trim_messages(state["messages"], max_tokens=MAX_TOKENS_CHECKPOINTER, token_counter=model,
                            strategy="last", start_on="human", include_system=False)
    response = model_with_tools.invoke([sys] + list(trimmed))
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

graph.add_node("memory",load_memory_node)
graph.add_node("brain", brain_node)
graph.add_node("tool_node", ToolNode(tools))
graph.add_node("kb_answer", kb_answer_node)

graph.add_edge(START, "memory")
graph.add_edge("memory","brain")
graph.add_conditional_edges("brain", should_continue)
graph.add_conditional_edges("tool_node", route_after_tools)
graph.add_edge("kb_answer", END)       

agent_graph = graph.compile(checkpointer=postgress_checkpointer,store=postgress_store)


if __name__ == "__main__":
    q = "what is the return policy of your company?"
    result = agent_graph.invoke(
        {"messages": [HumanMessage(content=q)], "query": q},
        config={"recursion_limit": 10},
    )
    print(result["messages"])