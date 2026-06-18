from langchain.tools import tool


from app.crud.order import get_order_by_id
from app.crud.order_item import get_items_by_order


@tool
def get_order_status(order_id: int) -> str:
    """Look up the current status and contents of a specific order by its numeric
    order id. Use when a customer asks about a particular order they placed."""
    order = get_order_by_id(order_id)
    if order is None:
        return f"No order found with id {order_id}."

    items = get_items_by_order(order_id)
    item_str = "; ".join(
        f"product {it.product_id} x{it.quantity} @ €{it.unit_price}" for it in items
    ) or "no items"

    return (f"Order {order.id}: status '{order.status}', total €{order.total_amount}, "
            f"placed {order.created_at:%Y-%m-%d}. Items: {item_str}.")





