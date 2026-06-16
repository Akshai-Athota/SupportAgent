from dotenv import load_dotenv
import os

load_dotenv()

class chatModel:
    groq_api_key = os.getenv("GROQ_API_KEY")
    model_name  = os.getenv("MODEL")


chat_model = chatModel()
