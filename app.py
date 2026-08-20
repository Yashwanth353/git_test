from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

app = FastAPI(title="OrderFlow API")


class OrderItem(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    customer_name: str
    items: List[OrderItem]


class Order(OrderCreate):
    order_id: str = ""
    status: str = "pending"


# In-memory store — pre-populated with two sample orders
orders_db: dict = {
    "ord-001": Order(
        order_id="ord-001",
        customer_name="Alice",
        status="pending",
        items=[OrderItem(product_id=1, quantity=2)],
    ),
    "ord-002": Order(
        order_id="ord-002",
        customer_name="Bob",
        status="delivered",
        items=[OrderItem(product_id=3, quantity=1)],
    ),
}


@app.get("/orders")
def get_orders(status: Optional[str] = Query(None)):
    # TODO: Return all orders as a list.
    # If the 'status' query param is provided, return only orders matching that status.
    orders=list(orders_db.values())

    if status is not None:
        orders = [order for order in orders if order.status== status]
    return orders


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    # TODO: Look up order_id in orders_db.
    # Return the order if found.
    # Raise HTTP 404 with a descriptive message if not found.
    if order_id not in orders_db:
        raise HTTPException(
            status_code=404,
            detail="order not found"
         )
    return orders_db[order_id]


@app.post("/orders", status_code=201)
def create_order(payload: OrderCreate):
    # TODO: Raise HTTP 422 if payload.items is empty.
    # Generate a new order_id using uuid4(),
    # create an Order object, save it to orders_db, and return it.
    if not payload.items:
        raise HTTPException(
            status_code=422,
            detail="order must contain at least one item"
        )
    new_order_id=str(uuid4())
    new_order=Order(
        order_id=new_order_id,
customer_name=payload.customer_name,
      status=payload.status,
      items=payload.items
    )

    orders_db[new_order_id]=new_order

    return new_order
