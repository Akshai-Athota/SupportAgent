from app.crud.db import get_session
from app.models.product import Product

def create_product(name, price, quantity, seller=None):
    with get_session() as session:
        product = Product(name=name, price=price, quantity=quantity, seller=seller)
        session.add(product)
        session.flush()
        return product

def get_products():
    with get_session() as session:
        return session.query(Product).all()

def get_product_by_id(product_id):
    with get_session() as session:
        return session.query(Product).filter_by(id=product_id).first()

def update_product(product_id, **fields):
    with get_session() as session:
        product = session.query(Product).filter_by(id=product_id).first()
        if product is None:
            return None
        for key, value in fields.items():
            setattr(product, key, value)
        session.flush()
        return product

def delete_product(product_id):
    with get_session() as session:
        product = session.query(Product).filter_by(id=product_id).first()
        if product is None:
            return False
        session.delete(product)
        return True