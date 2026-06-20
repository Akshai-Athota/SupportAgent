from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String, nullable=True)   
    email = Column(String, nullable=False,unique=True)
    password = Column(String,nullable=False)

    addresses = relationship("Address", back_populates="customer")
    orders = relationship("Order", back_populates="customer")
    conversations = relationship("Conversation",back_populates="customer",cascade="all, delete-orphan")