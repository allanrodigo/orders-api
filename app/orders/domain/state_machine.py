from app.orders.domain.models import OrderStatuses
from app.orders.domain.exceptions import InvalidStatusTransition, UnknownStatusError

ALLOWED_STATUSES_TRANSICTIONS = {
    OrderStatuses.created: {
        OrderStatuses.processing, 
        OrderStatuses.cancelled,
    },
    OrderStatuses.processing: {
        OrderStatuses.ready_to_ship,
        OrderStatuses.cancelled,
    },
    OrderStatuses.ready_to_ship: {
        OrderStatuses.shipped,
        OrderStatuses.cancelled
    },
    OrderStatuses.shipped: {
        OrderStatuses.delivered,
        OrderStatuses.cancelled,
    },
    OrderStatuses.delivered: {
        OrderStatuses.cancelled
    },
    OrderStatuses.cancelled: set()
}

def transition_status(current_status: OrderStatuses, new_status: OrderStatuses):
    if current_status not in ALLOWED_STATUSES_TRANSICTIONS:
        raise UnknownStatusError(f"Unknown status: {current_status.value()}")
    if new_status not in ALLOWED_STATUSES_TRANSICTIONS[current_status]:
        raise InvalidStatusTransition(f"invalid status transition: {current_status.value} -> {new_status.value}")
    
    return new_status