from pydantic import BaseModel
from enum import Enum


class OrderStatuses(str, Enum):
    created = "created"
    processing = "processing"
    ready_to_ship = "ready_to_ship"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"
    

class OrderRequest(BaseModel):
    amount: float
    comission_percentage: float


class Order(OrderRequest):
    code: str
    status: OrderStatuses
    comission: float
    

class UpdateOrderStatusRequest(BaseModel):
    status: OrderStatuses