from fastapi import HTTPException
from app.orders.domain.exceptions import InvalidStatusTransition, UnknownStatusError
from app.orders.domain.models import (
    OrderRequest, 
    Order,
    OrderStatuses,
)
from app.orders.domain.utils import calculate_comission
from app.orders.domain.state_machine import transition_status

ORDERS_COUNT = 0
ORDERS = {}


def create_order(order_request: OrderRequest) -> Order:
    global ORDERS_COUNT
    
    order_code = f"ORD{str(ORDERS_COUNT).zfill(7)}"
    commission = calculate_comission(
        order_request.amount,
        order_request.comission_percentage
    )
    order= Order(
        code=order_code,
        status=OrderStatuses.created,
        amount=order_request.amount,
        comission_percentage=order_request.comission_percentage,
        comission=commission,
    )
    ORDERS[order_code] = order
    ORDERS_COUNT += 1
    return order

def get_all_orders() -> list[Order]:
    return list(ORDERS.values())

def get_order_by_code(code: str):
    if code not in ORDERS:
        raise HTTPException(status_code=404, detail=f"code {code} not found")
    return ORDERS[code]

def update_order_status(code: str, new_status: OrderStatuses):
    order = get_order_by_code(code)
    try:
        order.status = transition_status(order.status, new_status)
    except InvalidStatusTransition as e:
        raise HTTPException(status_code=409, detail=str(e))
    except UnknownStatusError as e:
        raise HTTPException(status_code=422, detail=str(e))
        
    return order