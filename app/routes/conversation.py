import logging

from fastapi import APIRouter, Depends, HTTPException

from app.crud.conversation import (
    create_conversation as cc,
    get_all_conversations as gac,
    delete_conversation as dc,
)
from app.security.token_verification import get_current_customer

logger = logging.getLogger(__name__)

conversation_route = APIRouter(prefix="/conversation", tags=["conversations"])


@conversation_route.post("/create")
def create_conversation(title: str | None, customer_id: int = Depends(get_current_customer)):
    try:
        conversation = cc(customer_id=customer_id, title=title)
        return {"conversation_id": conversation.id, "title": conversation.title}
    except Exception:
        logger.exception("conversation_create_failed")
        raise HTTPException(status_code=500, detail="Conversation creation failed")


@conversation_route.get("/")
def get_all_conversations(customer_id: int = Depends(get_current_customer)):
    try:
        conversations = gac(customer_id=customer_id)
        return {
            "conversations": [
                {"conversation_id": c.id, "title": c.title, "updated_at": c.updated_at}
                for c in conversations
            ]
        }
    except Exception:
        logger.exception("conversation_fetch_failed")
        raise HTTPException(status_code=500, detail="Conversation fetch failed")


@conversation_route.delete("/{conversation_id}")
def delete(conversation_id: str, customer_id: int = Depends(get_current_customer)):
    try:
        deleted = dc(customer_id=customer_id, conversation_id=conversation_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return {"deleted": True, "conversation_id": conversation_id}
    except HTTPException:
        raise
    except Exception:
        logger.exception("conversation_delete_failed")
        raise HTTPException(status_code=500, detail="Conversation delete failed")