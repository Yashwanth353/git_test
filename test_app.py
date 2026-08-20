from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_get_all_orders():
    # TODO: Send GET /orders
    # Assert: status code is 200 and the response body is a non-empty list
    response =client.get("/orders")
    assert response.status_code==200
    assert response.json()


def test_get_orders_filter_by_status():
    # TODO: Send GET /orders?status=pending
    # Assert: status code is 200 and every order in the response has status == "pending"
    response =client.get("/orders?status=pending")
    assert response.status_code ==200
    assert all(order["status"]=="pending" for order in response.json())


def test_get_order_not_found():
    # TODO: Send GET /orders/invalid-id
    # Assert: status code is 404
    response=client.get("/orders/invalis-id")
    assert response.status_code==404


def test_create_order_success():
    # TODO: Send POST /orders with a valid payload (customer_name + non-empty items list)
    # Assert: status code is 201 and the response body contains an "order_id" field
    payload={
        "customer_name":"Test User",
        "items":[{
            "product_id":1,"quantity":2
        }]
    }
    response = client.post("/orders",json=payload)

    assert response.status_code==201
    assert "order_id" in response.json()


def test_create_order_empty_items():
    # TODO: Send POST /orders with items=[]
    # Assert: status code is 422
    payload={
        "customer_name":"Test User",
        "items":[]
    }
    response=client.post("/orders",json=payload)
    assert response.ststus_code==422