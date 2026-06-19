from langgraph.checkpoint.postgres import PostgresSaver
from app.config import DATABSE_URL

checkpointer_cm = PostgresSaver.from_conn_string(DATABSE_URL)
checkpointer = checkpointer_cm.__enter__()

checkpointer.setup()