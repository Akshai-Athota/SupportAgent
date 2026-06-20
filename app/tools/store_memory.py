from uuid import uuid4
from typing import Annotated
from langchain.tools import tool
from langgraph.prebuilt import InjectedState, InjectedStore
from langgraph.store.base import BaseStore

@tool
def save_memory(fact: str,
                state: Annotated[dict, InjectedState],
                store: Annotated[BaseStore, InjectedStore]) -> str:
    """Save a durable fact about the current customer for future conversations
    (a preference, recurring issue, or similar). Don't save one-off questions."""
    store.put(("memories", str(state["customer_id"])), str(uuid4()), {"text": fact})
    return "Noted."