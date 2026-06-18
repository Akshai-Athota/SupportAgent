from datetime import datetime, timezone

from langchain.tools import tool

from app.config import REFUND_THRESHOLD
from app.crud.order import get_order_by_id






@tool
def check_refund_eligibility(order_id: int) -> str:
    """Check whether an order qualifies for a refund. Returns eligibility and whether
    the refund needs manual human approval. Use when a customer requests a refund."""
    order = get_order_by_id(order_id)
    if order is None:
        return f"No order found with id {order_id}."

    placed = order.created_at

    if placed.tzinfo is None:
        placed = placed.replace(tzinfo=timezone.utc)
    days_old = (datetime.now(timezone.utc) - placed).days

    if order.status == "cancelled":
        return f"Order {order.id} is already cancelled; no refund applies."

    if days_old > 30:
        return (f"Order {order.id} is {days_old} days old, outside the 30-day return "
                f"window. Not eligible for a refund.")

    if float(order.total_amount) > REFUND_THRESHOLD:
        return (f"Order {order.id} (€{order.total_amount}) is within the return window but "
                f"exceeds the €{REFUND_THRESHOLD} auto-approval limit. Requires manual "
                f"approval — escalate to a human.")

    return (f"Order {order.id} (€{order.total_amount}) is within the return window and "
            f"eligible for an automatic refund.")


