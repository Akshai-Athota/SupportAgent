from langchain_groq import ChatGroq
from app.config import chat_model
from langchain_core.prompts import ChatPromptTemplate

model = ChatGroq(api_key=chat_model.groq_api_key, model=chat_model.model_name)

prompt = "You are an AI agent ,answer the user question with as short response as possible for testing queston : {question}"


llm = ChatPromptTemplate.from_template(prompt) | model

