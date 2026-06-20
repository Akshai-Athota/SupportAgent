from app.crud.db import get_session
from app.models.conversation import Conversation


def create_conversation(customer_id: int, title : str|None):
    with get_session() as session:
        if title is None:
            title = "New chat" + str(len(get_all_conversations(customer_id=customer_id))+1)
        conversation = Conversation(customer_id=customer_id,title=title)
        session.add(conversation)
        session.flush()
        return conversation

def get_all_conversations(customer_id:int):
    with get_session() as session:
        conversations=session.query(Conversation).filter_by(customer_id=customer_id).all()
        return conversations

def get_conversation(customer_id:int,conversation_id:str)->bool:
    with get_session() as session:
        conversation = session.query(Conversation).filter_by(customer_id=customer_id,id=conversation_id).first()

        if conversation is None:
            return False
        
        return True

def update_conversation(customer_id: int, conversation_id: str, **fields):
    with get_session() as session:
        conversation = session.query(Conversation).filter_by(
            customer_id=customer_id, id=conversation_id).first()
        if conversation is None:
            return None
        for key, value in fields.items():
            setattr(conversation, key, value)
        session.flush()
        return conversation


def delete_conversation(customer_id:int,conversation_id)->bool:
    with get_session() as session:
        conversation = session.query(Conversation).filter_by(customer_id=customer_id,id=conversation_id).first()

        if conversation is None:
            return False

        session.delete(conversation)
        return True
