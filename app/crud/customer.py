from app.crud.db import get_session
from app.models.customer import Customer

def create_customer(first_name, last_name, phone_number=None, email=None):
    with get_session() as session:
        customer = Customer(first_name=first_name, last_name=last_name,
                            phone_number=phone_number, email=email)
        session.add(customer)
        session.flush()
        return customer

def get_customers(session=None):
    with get_session() as session:
        return session.query(Customer).all()

def get_customer_by_id(customer_id):
    with get_session() as session:
        return session.query(Customer).filter_by(id=customer_id).first()

def get_customer_by_email(email):
    with get_session() as session:
        return session.query(Customer).filter_by(email=email).first()

def update_customer(customer_id, **fields):
    with get_session() as session:
        customer = session.query(Customer).filter_by(id=customer_id).first()
        if customer is None:
            return None
        for key, value in fields.items():
            setattr(customer, key, value)
        session.flush()
        return customer

def delete_customer(customer_id):
    with get_session() as session:
        customer = session.query(Customer).filter_by(id=customer_id).first()
        if customer is None:
            return False
        session.delete(customer)
        return True
    

