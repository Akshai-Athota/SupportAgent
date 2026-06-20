from app.models.base import Base

from uuid import uuid4
from sqlalchemy import Column,String,Integer,ForeignKey ,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime,timezone

class Conversation(Base):
    __tablename__="conversation"

    id = Column(String,default=lambda:str(uuid4()),primary_key=True)
    title = Column(String(200),nullable=False,default="New Chat")
    customer_id = Column(Integer,ForeignKey("customer.id"),nullable=False)
    created_at = Column(DateTime(timezone=True),default=lambda : datetime.now(timezone.utc))
    updated_at = Column( DateTime(timezone=True),default=lambda: datetime.now(timezone.utc),onupdate=lambda: datetime.now(timezone.utc),nullable=False,)
    customer = relationship("Customer",back_populates="conversations")

