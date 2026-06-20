
import random

from app.crud.db import init_db

from app.crud.product import create_product
from app.crud.customer import create_customer
from app.crud.address import create_address
from app.crud.order import create_order

random.seed(42)

PRODUCTS = [
    {"name": "Wireless Headphones",  "price": 79,  "quantity": 120, "seller": "AudioPlus"},
    {"name": "Laptop Stand",         "price": 35,  "quantity": 80,  "seller": "DeskGear"},
    {"name": "Mechanical Keyboard",  "price": 119, "quantity": 60,  "seller": "KeyWorks"},
    {"name": "USB-C Hub",            "price": 45,  "quantity": 200, "seller": "ConnectIt"},
    {"name": "4K Monitor",           "price": 349, "quantity": 40,  "seller": "ViewMax"},
    {"name": "Laptop 14-inch",       "price": 899, "quantity": 25,  "seller": "CompuWorld"},
    {"name": "HD Webcam",            "price": 65,  "quantity": 90,  "seller": "ConnectIt"},
    {"name": "Office Chair",         "price": 199, "quantity": 30,  "seller": "ComfortSeat"},
]

CUSTOMERS = [
    {"first_name": "Anna",   "last_name": "Schmidt",  "email": "anna.schmidt@example.com",   "phone_number": "+491234567890","password":"abcd123"},
    {"first_name": "Liam",   "last_name": "Becker",   "email": "liam.becker@example.com",    "phone_number": "+491234567890","password":"abcd123"},
    {"first_name": "Sophie", "last_name": "Wagner",   "email": "sophie.wagner@example.com",  "phone_number": "+491234567890","password":"abcd123"},
    {"first_name": "Noah",   "last_name": "Fischer",  "email": "noah.fischer@example.com",   "phone_number": "+491234567890","password":"abcd123"},
    {"first_name": "Mia",    "last_name": "Weber",    "email": "mia.weber@example.com",      "phone_number": "+491234567890","password":"abcd123"},
    {"first_name": "Lucas",  "last_name": "Hoffmann", "email": "lucas.hoffmann@example.com", "phone_number": "+491234567890","password":"abcd123"},
    {"first_name": "Emma",   "last_name": "Schulz",   "email": "emma.schulz@example.com",    "phone_number": "+491234567890","password":"abcd123"},
    {"first_name": "Ben",    "last_name": "Koch",     "email": "ben.koch@example.com",       "phone_number": "+491234567890","password":"abcd123"},
    {"first_name": "Lena",   "last_name": "Richter",  "email": "lena.richter@example.com",   "phone_number": "+491234567890","password":"abcd123"},
    {"first_name": "Paul",   "last_name": "Wolf",     "email": "paul.wolf@example.com",      "phone_number": "+491234567890","password":"abcd123"},
]

STATUSES = ["processing", "shipped", "delivered", "cancelled"]
STREETS  = ["Hauptstrasse", "Bahnhofstrasse", "Gartenweg", "Lindenallee"]
CITIES   = ["Berlin", "Munich", "Hamburg", "Cologne"]


def seed():
    init_db()

    products = [] 
    for p in PRODUCTS:
        product = create_product(**p)
        products.append((product.id, p["price"]))

    customer_ids = []
    for c in CUSTOMERS:
        customer = create_customer(**c)
        customer_ids.append(customer.id)
        create_address(
            customer_id=customer.id,
            house_number=random.randint(1, 200),
            street_name=random.choice(STREETS),
            city=random.choice(CITIES),
            state=random.choice(CITIES),
            country="Germany",
            pincode=str(random.randint(10000, 99999)),
        )

    for _ in range(25):
        chosen = random.sample(products, k=random.randint(1, 3))
        items, total = [], 0
        for pid, price in chosen:
            qty = random.randint(1, 2)
            items.append({"product_id": pid, "quantity": qty, "unit_price": price})
            total += qty * price
        create_order(
            customer_id=random.choice(customer_ids),
            items=items,
            total_amount=total,
            status=random.choice(STATUSES),
        )

    
    laptop_id, laptop_price = products[5]
    create_order(
        customer_id=customer_ids[0],
        items=[{"product_id": laptop_id, "quantity": 1, "unit_price": laptop_price}],
        total_amount=laptop_price,
        status="delivered",
    )

    print("Seed complete: products, customers, addresses, and ~26 orders inserted.")


if __name__ == "__main__":
    seed()