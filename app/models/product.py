from sqlalchemy import Column,String,Integer

from app.models.base import Base


class Product(Base):
    __tablename__="product"

    id=Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    seller = Column(String)