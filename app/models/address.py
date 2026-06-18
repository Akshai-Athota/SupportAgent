from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))   # the FK column
    house_number = Column(Integer)
    street_name = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    pincode = Column(String)

    customer = relationship("Customer", back_populates="addresses")