from langgraph.store.postgres import PostgresStore
from psycopg_pool import ConnectionPool
from app.config import DATABSE_URL

pool = ConnectionPool(
    conninfo=DATABSE_URL,
    max_size=20,
    kwargs={"autocommit": True, "prepare_threshold": 0},
    check=ConnectionPool.check_connection,   
)

storepointer = PostgresStore(pool)


storepointer.setup()