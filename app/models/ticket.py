from app.models.base import Base

from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from uuid import uuid4

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    customer_id = Column(Integer, ForeignKey("customer.id"))
    conversation_id = Column(String, ForeignKey("conversation.id"))
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status = Column(String, default="open", nullable=False)
    summary = Column(String, nullable=True)

    customer = relationship("Customer", back_populates="tickets")
    conversation = relationship("Conversation", back_populates="tickets")