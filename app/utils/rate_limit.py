from slowapi import Limiter
from slowapi.util import get_remote_address

def get_rate_limiter(request):
    api_key = request.headers.get("X-API-Key")

    if api_key:
        return api_key
    
    return get_remote_address(request)

limiter = Limiter(key_func=get_rate_limiter)