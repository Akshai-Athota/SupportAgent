import jwt
import os
from datetime import datetime,timedelta,timezone

from app.config import JWT_SECRET,JWT_ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(customer_id:int,email:str)->str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub":str(customer_id),"email":email,"exp":expire}
    return jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGORITHM)

def decode_token(token:str)->dict:
    return jwt.decode(jwt=token,key=JWT_SECRET,algorithms=[JWT_ALGORITHM])