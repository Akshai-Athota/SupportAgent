from fastapi import APIRouter,Depends

from app.crud.ticket import get_all_tickets as gt,create_ticket as ct,update_ticket as ut,delete_ticket as dt
from app.security.token_verification import get_current_customer

route = APIRouter(prefix="/ticket",tags=["tickets"])

def _ticket_dict(t):
    return {"id": t.id, "conversation_id": t.conversation_id,
            "summary": t.summary, "status": t.status, "created_at": t.created_at}


@route.post("/")
def create_ticket(conversation_id:str,customer_id:int=Depends(get_current_customer)):
    ticket = ct(conversation_id=conversation_id,customer_id=customer_id)
    return _ticket_dict(ticket)

@route.get("/")
def get_all_tickets(customer_id: int = Depends(get_current_customer)):
    return {"tickets": [_ticket_dict(t) for t in gt(customer_id=customer_id)]}

@route.put("/")
def update_tickets(ticket_id: str, status: str, customer_id: int = Depends(get_current_customer)):
    ticket = ut(customer_id=customer_id, ticket_id=ticket_id, status=status)
    return _ticket_dict(ticket) if ticket else {"error": "not found"}

@route.delete("/")
def delete_ticket(ticket_id:str,customer_id:int=Depends(get_current_customer)):
    return dt(customer_id=customer_id,ticket_id=ticket_id)