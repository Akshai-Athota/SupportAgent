from fastapi import APIRouter,HTTPException


from app.crud.customer import create_customer,get_customer_by_email
from app.utils.password import hash_password,verify_password
from app.utils.jwt_utils import create_access_token
from app.schemas.auth_schema import SignupRequest,LoginRequest,TokenResponse


auth = APIRouter(tags=["auth"])


@auth.post("/signup")
def signup(request:SignupRequest)->TokenResponse:
    if get_customer_by_email(request.email):
        raise HTTPException(status_code=409, detail="Email already registered")

    
    customer = create_customer(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        password=hash_password(request.password),
        phone_number=request.phone_number
    )

    return TokenResponse(access_token=create_access_token(customer_id=customer.id,email=customer.email))


@auth.post("/login")
def login(request:LoginRequest)->TokenResponse:
    customer = get_customer_by_email(request.email)
    if not customer or not customer.password or not verify_password(request.password, customer.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return TokenResponse(access_token=create_access_token(customer_id=customer.id,email=customer.email))
