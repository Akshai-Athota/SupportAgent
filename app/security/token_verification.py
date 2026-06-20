import jwt
from fastapi import HTTPException,Depends
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
import logging

from app.utils.jwt_utils import decode_token

bearer_schema = HTTPBearer(auto_error=False)
logger = logging.getLogger(__name__)


def get_current_customer(credentials : HTTPAuthorizationCredentials = Depends(bearer_schema))->int:
    if credentials is None:
        raise HTTPException("No token present")
    

    try:
        payload = decode_token(credentials.credentials)

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError as e:
        logger.warning(f"jwt decode failed: {type(e).__name__}: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

    customer_id = payload.get("sub")

    if customer_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return int(customer_id)
