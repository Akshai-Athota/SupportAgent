import logging

from fastapi import APIRouter, Depends, HTTPException

from app.crud.demo import seed_orders_for_customer
from app.crud.order import get_orders_by_customer
from app.security.token_verification import get_current_customer

logger = logging.getLogger(__name__)

demo_route = APIRouter(prefix="/demo", tags=["demo"])

MAX_ORDERS_PER_CUSTOMER = 10


@demo_route.post("/seed-orders")
def seed_orders(count: int = 4, customer_id: int = Depends(get_current_customer)):
    count = max(1, min(count, 5))                       

    existing = get_orders_by_customer(customer_id)
    if len(existing) >= MAX_ORDERS_PER_CUSTOMER:
        raise HTTPException(status_code=409,
                            detail="You already have enough sample orders.")
    try:
        return seed_orders_for_customer(customer_id, num_orders=count)
    except Exception:
        logger.exception("seed_orders_failed")
        raise HTTPException(status_code=500, detail="Failed to create sample orders")