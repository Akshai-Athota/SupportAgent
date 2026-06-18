from app.crud.db import get_session
from app.models.order_item import OrderItem

def create_order_item(order_id, product_id, quantity, unit_price):
    with get_session() as session:
        item = OrderItem(order_id=order_id, product_id=product_id,
                         quantity=quantity, unit_price=unit_price)
        session.add(item)
        session.flush()
        return item

def get_order_item_by_id(item_id):
    with get_session() as session:
        return session.query(OrderItem).filter_by(id=item_id).first()

def get_items_by_order(order_id):
    with get_session() as session:
        return session.query(OrderItem).filter_by(order_id=order_id).all()

def update_order_item(item_id, **fields):
    with get_session() as session:
        item = session.query(OrderItem).filter_by(id=item_id).first()
        if item is None:
            return None
        for key, value in fields.items():
            setattr(item, key, value)
        session.flush()
        return item

def delete_order_item(item_id):
    with get_session() as session:
        item = session.query(OrderItem).filter_by(id=item_id).first()
        if item is None:
            return False
        session.delete(item)
        return True