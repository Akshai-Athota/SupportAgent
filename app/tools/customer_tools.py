from typing import Annotated

from langchain.tools import tool
from langgraph.prebuilt import InjectedState

from app.crud.customer import get_customer_by_id


@tool
def get_current_customer(state: Annotated[dict, InjectedState]) -> str:
    """Get the profile (name, email) of the currently logged-in customer."""
    c = get_customer_by_id(state["customer_id"])
    if c is None:
        return "Customer profile not found."
    return f"{c.first_name} {c.last_name}, email {c.email}, customer id {c.id}."


