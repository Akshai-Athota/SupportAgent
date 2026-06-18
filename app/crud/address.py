from app.crud.db import get_session
from app.models.address import Address

def create_address(customer_id,house_number,street_name,city,state,country,pincode):
    with get_session() as session:
        address = Address(
            customer_id=customer_id,
            house_number=house_number,
            street_name=street_name,
            city=city,state=state,
            country=country,
            pincode=pincode
        )
        session.add(address)
        session.flush()
        return address

def get_address():
    with get_session() as session:
        addresses = session.query(Address).all()
        return addresses

def get_address_by_id(address_id):
    with get_session() as session:
        address= session.query(Address).filter_by(id=address_id).first()
        return address

def get_address_by_customer_id(customer_id):
    with get_session() as session:
        addresses = session.query(Address).filter_by(customer_id=customer_id).all()
        return addresses


def update_address(address_id, **fields):
    with get_session() as session:
        address = session.query(Address).filter_by(id=address_id).first()
        if address is None:
            return None
        for key, value in fields.items():
            setattr(address, key, value)
        session.flush()
        return address

def delete_address(address_id):
    with get_session() as session:
        address = session.query(Address).filter_by(id=address_id).first()
        if address is None:
            return False
        session.delete(address)
        return True