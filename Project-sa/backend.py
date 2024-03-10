from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Define Models
class User(BaseModel):
    username: str
    password: str

class Company(BaseModel):
    name: str
    gst_number: str

class Item(BaseModel):
    name: str
    quantity: int

class Customer(BaseModel):
    name: str
    address: str
    contact: str
    email: str

class Order(BaseModel):
    from_company: Company
    to_company: Company
    product_name: str
    description: str
    quantity: int
    taxes: str

class Invoice(BaseModel):
    company: Company
    order: Order

# Sample Data
users = {
    "user1": User(username="user1", password="password1"),
    "user2": User(username="user2", password="password2"),
    "user3": User(username="user3", password="password3")
}

items = [
    Item(name="Item 1", quantity=10),
    Item(name="Item 2", quantity=20)
]

# Authentication
def authenticate_user(user: User):
    if user.username in users and users[user.username].password == user.password:
        return True
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

# FastAPI Endpoints
@app.post("/login")
async def login(user: User):
    authenticate_user(user)
    return {"message": "Login successful"}

@app.post("/increase_stock/{item_name}")
async def increase_stock(item_name: str, quantity: int, user: User = Depends(authenticate_user)):
    item = next((x for x in items if x.name == item_name), None)
    if item:
        item.quantity += quantity
        return {"message": f"Stock of {item_name} increased by {quantity}"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@app.post("/decrease_stock/{item_name}")
async def decrease_stock(item_name: str, quantity: int, user: User = Depends(authenticate_user)):
    item = next((x for x in items if x.name == item_name), None)
    if item:
        if item.quantity >= quantity:
            item.quantity -= quantity
            return {"message": f"Stock of {item_name} decreased by {quantity}"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@app.post("/generate_invoice")
async def generate_invoice(customer: Customer, order: Order, user: User = Depends(authenticate_user)):
    return Invoice(company=order.from_company, order=order)
