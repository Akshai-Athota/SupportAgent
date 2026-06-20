from typing import Annotated
from datetime import datetime, timezone

from langchain.tools import tool
from langgraph.prebuilt import InjectedState

from app.config import REFUND_THRESHOLD
from app.crud.order import get_order_by_id




@tool
def check_my_refund_eligibility(order_id: int|str, state: Annotated[dict, InjectedState]) -> str:
    """Check refund eligibility for one of the current customer's orders."""
    order_id = int(order_id)
    order = get_order_by_id(order_id)
    if order is None or order.customer_id != state["customer_id"]:
        return f"No order {order_id} found on your account."
    placed = order.created_at
    if placed.tzinfo is None:
        placed = placed.replace(tzinfo=timezone.utc)
    days_old = (datetime.now(timezone.utc) - placed).days
    if order.status == "cancelled":
        return f"Order {order.id} is already cancelled; no refund applies."
    if days_old > 30:
        return f"Order {order.id} is {days_old} days old, outside the 30-day return window. Not eligible."
    if float(order.total_amount) > REFUND_THRESHOLD:
        return f"Order {order.id} (€{order.total_amount}) exceeds the €{REFUND_THRESHOLD} auto-approval limit. Escalate to a human agent."
    return f"Order {order.id} (€{order.total_amount}) is within the return window and eligible for an automatic refund."


