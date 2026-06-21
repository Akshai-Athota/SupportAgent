from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from app.config import DATABSE_URL
import app.models

engine  = create_engine(url=DATABSE_URL,echo=False,pool_pre_ping=True,connect_args={"connect_timeout":20})

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
        raise
    finally:
        session.close()


def init_db():

    from app.models.base import Base

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


