from typing import Annotated
from langchain.tools import tool
from langgraph.prebuilt import InjectedState

from app.crud.ticket import create_ticket as ct,get_all_tickets_by_order_id,get_all_tickets
from app.crud.order import get_order_by_id,get_orders_by_customer


@tool
def escalate_to_human(reason: str, state: Annotated[dict, InjectedState], order_id: int | str|None = None) -> str:
    """Escalate the current issue to a human by creating a support ticket. Use when a refund
    needs manual approval, you can't resolve the issue, or the customer asks for a human.
    Pass order_id if the issue concerns a specific order. `reason` is a one-line summary."""
    ticket = ct(customer_id=state["customer_id"], conversation_id=state["conversation_id"],
                summary=reason, order_id=order_id)
    return f"I've escalated this to our team (ticket {ticket.id}); a human agent will follow up."


@tool
def get_my_tickets_of_order(state: Annotated[dict, InjectedState], order_id: int | str | None = None) -> str:
    """List of customer tickets of all orders if there is no order id provided or list the current
    customer's support tickets with their status of the corresponding order.
    Use when the customer asks about the status of their tickets, escalations, or a ticket for a specific order."""

    all_tickets = []

    if order_id is None:
        orders = get_orders_by_customer(state["customer_id"])
        for order in orders:
            all_tickets.append(get_all_tickets_by_order_id(order.id))
    else:
        try:
            order_id = int(order_id)
        except (TypeError, ValueError):
            return f"'{order_id}' isn't a valid order id."

        order = get_order_by_id(order_id)
        if order is None or order.customer_id != state["customer_id"]:
            return f"No order {order_id} found on your account."

        all_tickets.append(get_all_tickets_by_order_id(order_id))

    tickets = [t for group in all_tickets for t in group]

    if not tickets:
        return "You have no support tickets."

    return "; ".join(
        f"ticket {t.id[:8]} (status: {t.status}, order: {t.order_id or 'n/a'}) — {t.summary}"
        for t in tickets
    )