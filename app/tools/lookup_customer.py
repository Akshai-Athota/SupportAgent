from langchain.tools import tool

from app.crud.order import  get_orders_by_customer
from app.crud.customer import get_customer_by_email


@tool
def lookup_customer(email: str) -> str:
    """Find a customer by their email address and list their orders. Use to identify
    a customer or to see their order history before answering account questions."""
    customer = get_customer_by_email(email)
    if customer is None:
        return f"No customer found with email {email}."

    orders = get_orders_by_customer(customer.id)
    order_str = "; ".join(
        f"#{o.id} ({o.status}, €{o.total_amount})" for o in orders
    ) or "no orders"

    return (f"Customer {customer.first_name} {customer.last_name} "
            f"(id {customer.id}, {customer.email}). Orders: {order_str}.")

