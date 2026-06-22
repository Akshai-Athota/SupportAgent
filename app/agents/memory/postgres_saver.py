from psycopg_pool import  ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver
from app.config import DATABSE_URL


pool = ConnectionPool(
    conninfo=DATABSE_URL,
    max_size=20,
    kwargs={"autocommit": True, "prepare_threshold": 0},
    check=ConnectionPool.check_connection,   
)

checkpointer = PostgresSaver(pool)


checkpointer.setup()