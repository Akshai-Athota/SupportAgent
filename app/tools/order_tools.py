from typing import Annotated

from langchain.tools import tool
from langgraph.prebuilt import InjectedState

from app.crud.order import get_order_by_id, get_orders_by_customer
from app.crud.order_item import get_items_by_order



@tool
def get_my_orders(state: Annotated[dict, InjectedState]) -> str:
    """List the orders belonging to the currently logged-in customer.
    Use when the customer refers to 'my orders' without giving an id."""
    orders = get_orders_by_customer(state["customer_id"])
    if not orders:
        return "You have no orders on record."
    return "; ".join(f"#{o.id} ({o.status}, €{o.total_amount})" for o in orders)


@tool
def get_my_order_status(order_id: int | str, state: Annotated[dict, InjectedState]) -> str:
    """Get the status of one of the current customer's orders by id."""
    order_id = int(order_id)
    order = get_order_by_id(order_id)
    if order is None or order.customer_id != state["customer_id"]:
        return f"No order {order_id} found on your account."
    items = get_items_by_order(order_id)
    item_str = "; ".join(f"product {it.product_id} x{it.quantity} @ €{it.unit_price}" for it in items) or "no items"
    return f"Order {order.id}: status '{order.status}', total €{order.total_amount}, placed {order.created_at:%Y-%m-%d}. Items: {item_str}."


