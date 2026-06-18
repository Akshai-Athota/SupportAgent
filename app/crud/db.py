from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from app.config import DATABSE_URL

engine  = create_engine(url=DATABSE_URL,echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False
)

@contextmanager
def get_session():
    session = SessionLocal()

    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()


def init_db():
    from app.models.base import Base
    from app.models import (
        address,
        customer,
        order_item,
        order,
        product
    )

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)