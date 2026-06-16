from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.llm import llm

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {'message':'alive'}


class chatRequest(BaseModel):
    query: str

class chatResponse(BaseModel):
    response : str

@app.post("/chat")
def get_ai_message(request:chatRequest)->chatResponse :
    result = llm.invoke({"question": request.query})
    print(result)
    return chatResponse(response=result.content)
