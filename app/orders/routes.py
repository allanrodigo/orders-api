from fastapi import FastAPI
from app.orders.domain.models import OrderRequest, UpdateOrderStatusRequest
from app.orders.service import create_order, get_all_orders, get_order_by_code, update_order_status

app = FastAPI()

@app.post("/orders", status_code=201)
async def create(order_request: OrderRequest):
    return create_order(order_request=order_request)

@app.get("/orders")
async def search():
    return get_all_orders()

@app.get("/orders/{code}")
async def fetch(code: str):
    return get_order_by_code(code=code)

@app.patch("/orders/{code}")
async def partial_update(code: str, order_status: UpdateOrderStatusRequest):
    return update_order_status(code, order_status.status)