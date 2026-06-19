from pydantic import BaseModel,Field
from typing import List

class chatRequest(BaseModel):
    query: str = Field(min_length=1,max_length=2000)

class chatResponse(BaseModel):
    response:str
    tools_used:List[str]