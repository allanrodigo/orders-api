# Orders API

Order management API built with **FastAPI** and Python 3.12. Allows creating orders, listing all orders, retrieving by order code, and updating order status following valid transition rules.

---

## Project Structure

```
.
├── main.py
├── Makefile
├── poetry.lock
├── pyproject.toml
└── app
    └── orders
        ├── routes.py
        ├── service.py
        └── domain
            ├── exceptions.py
            ├── models.py
            ├── state_machine.py
            └── utils.py
```

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/allanrodigo/orders-api.git
cd orders-api
```

**2. Install dependencies with Poetry**

```bash
poetry install
```

**3. Activate the virtual environment**

```bash
poetry env activate
```

---

## Running the API

Via Makefile:

```bash
make run
```

Or directly with Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

---

## Endpoints

### POST `/orders/` — Create Order

**Request Body**

```json
{
  "amount": 150.0,
  "comission_percentage": 10.0
}
```

**Response** `201 Created`

```json
{
  "code": "ORD0000000",
  "status": "created",
  "amount": 150.0,
  "comission_percentage": 10.0,
  "comission": 15.0
}
```

---

### GET `/orders/` — List All Orders

**Response** `200 OK`

```json
[
  {
    "code": "ORD0000000",
    "status": "created",
    "amount": 150.0,
    "comission_percentage": 10.0,
    "comission": 15.0
  }
]
```

---

### GET `/orders/{code}` — Retrieve Order by Code

**Response** `200 OK`

```json
{
  "code": "ORD0000000",
  "status": "created",
  "amount": 150.0,
  "comission_percentage": 10.0,
  "comission": 15.0
}
```

**Response** `404 Not Found`

```json
{
  "detail": "Order with code 'ORD9999999' not found"
}
```

---

### PATCH `/orders/{code}` — Update Order Status

**Request Body**

```json
{
  "status": "processing"
}
```

**Response** `200 OK`

```json
{
  "code": "ORD0000000",
  "status": "processing",
  "amount": 150.0,
  "comission_percentage": 10.0,
  "comission": 15.0
}
```

**Possible errors**

| HTTP Code | Reason                                              |
|-----------|-----------------------------------------------------|
| `409`     | Invalid transition (e.g. `created -> delivered`)    |
| `422`     | Unknown status (e.g. `shippedd`)                    |
| `404`     | Order not found (e.g. `ORD9999999`)                 |

---

## Status Transition Rules

| Current Status    | Allowed Transitions               |
|-------------------|-----------------------------------|
| `created`         | `processing`, `cancelled`         |
| `processing`      | `ready_to_ship`, `cancelled`      |
| `ready_to_ship`   | `shipped`, `cancelled`            |
| `shipped`         | `delivered`, `cancelled`          |
| `delivered`       | `cancelled`                       |
| `cancelled`       | —                                 |

---

## Dependencies

| Package   | Description                      |
|-----------|----------------------------------|
| Python    | 3.12                             |
| FastAPI   | Async web framework              |
| Uvicorn   | ASGI server                      |
| Poetry    | Dependency management            |

---

## Notes

- Order codes are generated sequentially: `ORD0000000`, `ORD0000001`, ...
- Commission calculation is handled by the `calculate_comission` function in `app/orders/domain/utils.py`.
- All status transitions are validated by `state_machine.py`.
- API responses are serializable via Pydantic or `dict`.