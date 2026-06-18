from app.config import chat_model
from app.agents.prompts.support_agent_prompt import support_agent_prompt

from langchain_groq import ChatGroq


model = ChatGroq(api_key=chat_model.groq_api_key, model=chat_model.model_name)


kb_chain = support_agent_prompt | model

