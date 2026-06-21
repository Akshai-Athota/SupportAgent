from typing import Annotated
from langchain.tools import tool
from langgraph.prebuilt import InjectedState

from app.crud.ticket import create_ticket as ct,get_all_tickets_by_order_id


@tool
def escalate_to_human(reason: str, state: Annotated[dict, InjectedState], order_id: int | None = None) -> str:
    """Escalate the current issue to a human by creating a support ticket. Use when a refund
    needs manual approval, you can't resolve the issue, or the customer asks for a human.
    Pass order_id if the issue concerns a specific order. `reason` is a one-line summary."""
    ticket = ct(customer_id=state["customer_id"], conversation_id=state["conversation_id"],
                summary=reason, order_id=order_id)
    return f"I've escalated this to our team (ticket {ticket.id}); a human agent will follow up."

from app.crud.ticket import get_all_tickets

@tool
def get_my_tickets_of_order(order_id:int|str,state: Annotated[dict, InjectedState]) -> str:
    """List the current customer's support tickets with their status of the corresponding order. Use when the customer
    asks about the status of their tickets, escalations, or a ticket for a specific order."""
    order_id = int(order_id)

    order = get_order_by_id(order_id)
    if order is None or order.customer_id != state["customer_id"]:
        return f"No order {order_id} found on your account."

    tickets = get_all_tickets_by_order_id(state["customer_id"])
    if not tickets:
        return "You have no support tickets."
    return "; ".join(
        f"ticket {t.id[:8]} (status: {t.status}, order: {t.order_id or 'n/a'}) — {t.summary}"
        for t in tickets
    )