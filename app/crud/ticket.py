from app.models.ticket import Ticket
from app.crud.db import get_session

def create_ticket(customer_id:int,conversation_id:str,summary:str="",order_id=None):
    if order_id:
        order_id = int(order_id)
    with get_session() as session:
        ticket = Ticket(
            customer_id=customer_id,
            conversation_id=conversation_id,
            summary=summary,
            order_id=order_id
        )
        session.add(ticket)
        session.flush()
        return ticket


def get_all_tickets(customer_id:int):
    with get_session() as session:
        return session.query(Ticket).filter_by(customer_id=customer_id).all()

def get_all_tickets_by_order_id(order_id:int):
    with get_session() as session:
        return session.query(Ticket).filter_by(order_id=order_id).all()

def get_ticket(customer_id:int,ticket_id:str):
    with get_session() as session:
        ticket = session.query(Ticket).filter_by(id=ticket_id,customer_id=customer_id).first()
        if ticket is None:
            return None
        return ticket

def update_ticket(customer_id:int,ticket_id:str,**fields):
    with get_session() as session:
        ticket = session.query(Ticket).filter_by(id=ticket_id,customer_id=customer_id).first()
        if ticket is None:
            return None
        for key,value in fields.items():
            setattr(ticket,key,value)
        session.flush()
        return ticket

def delete_ticket(customer_id:int,ticket_id:str)->bool:
    with get_session() as session:
        ticket = session.query(Ticket).filter_by(id=ticket_id,customer_id=customer_id).first()
        if ticket is None:
            return False
        session.delete(ticket)
        return True