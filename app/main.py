import os
import time
import uuid
import logging
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler



from app.routes.chat import chat_route
from app.routes.auth import auth as auth_route
from app.routes.conversation import conversation_route



from app.utils.rate_limit import limiter
from app.logging.config import setup_logging


setup_logging(level=os.getenv("LOG_LEVEL", "INFO"))   

logger = logging.getLogger("app.request")


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


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        logger.exception("request_failed", extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "duration_ms": duration_ms,
        })
        raise
    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    logger.info("request", extra={
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "duration_ms": duration_ms,
    })
    response.headers["X-Request-ID"] = request_id
    return response

app.state.limiter=limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)


app.include_router(auth_route)
app.include_router(chat_route)
app.include_router(conversation_route)


@app.get("/health")
@app.get("/")
def health():
    return {'message':'alive'}



