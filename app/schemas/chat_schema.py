from pydantic import BaseModel
from typing import List

class chatRequest(BaseModel):
    query: str

class chatResponse(BaseModel):
    response:str
    source:List[str]
    intent:List[str]
    category:List[str]