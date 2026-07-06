import random

from app.crud.db import get_session
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem

STATUSES = ["processing", "shipped", "delivered", "cancelled"]


def seed_orders_for_customer(customer_id: int, num_orders: int = 4):
    with get_session() as session:
        products = session.query(Product).all()
        if not products:
            return {"created": 0, "detail": "No products available to build orders."}

        created = []
        for _ in range(num_orders):
            chosen = random.sample(products, k=min(random.randint(1, 3), len(products)))
            order = Order(customer_id=customer_id, status=random.choice(STATUSES), total_amount=0)
            session.add(order)
            session.flush()                      # get order.id

            total = 0
            for p in chosen:
                qty = random.randint(1, 2)
                session.add(OrderItem(order_id=order.id, product_id=p.id,
                                      quantity=qty, unit_price=p.price))
                total += qty * p.price
            order.total_amount = total
            session.flush()
            created.append({"order_id": order.id, "status": order.status, "total": total})

        return {"created": len(created), "orders": created}