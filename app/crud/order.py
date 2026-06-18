from app.crud.db import get_session
from app.models.order import Order
from app.models.order_item import OrderItem

def create_order(customer_id, items, total_amount=None, status="processing"):
    # items: list of dicts -> {"product_id": .., "quantity": .., "unit_price": ..}
    with get_session() as session:
        order = Order(customer_id=customer_id, status=status, total_amount=total_amount)
        session.add(order)
        session.flush()  # assigns order.id before we attach items
        for item in items:
            session.add(OrderItem(
                order_id=order.id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
            ))
        session.flush()
        return order

def get_order_by_id(order_id):
    with get_session() as session:
        return session.query(Order).filter_by(id=order_id).first()

def get_orders_by_customer(customer_id):
    with get_session() as session:
        return session.query(Order).filter_by(customer_id=customer_id).all()

def update_order_status(order_id, status):
    with get_session() as session:
        order = session.query(Order).filter_by(id=order_id).first()
        if order is None:
            return None
        order.status = status
        session.flush()
        return order

def delete_order(order_id):
    with get_session() as session:
        order = session.query(Order).filter_by(id=order_id).first()
        if order is None:
            return False
        session.delete(order)  
        return True
    
