from langgraph.store.postgres import PostgresStore

from app.config import DATABSE_URL

store_cm = PostgresStore.from_conn_string(DATABSE_URL)
storepointer = store_cm.__enter__()

storepointer.setup()