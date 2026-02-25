# Orders API

API de gerenciamento de pedidos construída com **FastAPI** e Python. Permite criar pedidos, listar todos, consultar por código e atualizar o status seguindo regras de transição válidas.

---

## Estrutura do Projeto

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

## Instalação

**1. Clone o repositório**

```bash
git clone https://github.com/allanrodigo/orders-api.git
cd orders-api
```

**2. Instale as dependências com Poetry**

```bash
poetry install
```

**3. Ative o ambiente virtual**

```bash
poetry env activate
```

---

## Executando a API

Via Makefile:

```bash
make run
```

Ou diretamente com Uvicorn:

```bash
uvicorn main:app --reload
```

A API estará disponível em: `http://127.0.0.1:8000`

---

## Endpoints

### POST `/orders/` — Criar Pedido

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

### GET `/orders/` — Listar Todos os Pedidos

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

### GET `/orders/{code}` — Consultar Pedido por Código

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
  "detail": "code 'ORD9999999' not found"
}
```

---

### PATCH `/orders/{code}` — Atualizar Status do Pedido

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

**Erros possíveis**

| Código HTTP | Motivo                                        |
|-------------|-----------------------------------------------|
| `409`       | Transição inválida (ex: `created -> delivered`) |
| `422`       | Status desconhecido (ex: `shippedd`)          |
| `404`       | Pedido não encontrado (ex: `ORD9999999`)      |

---

## Regras de Transição de Status

| Status Atual      | Transições Permitidas             |
|-------------------|-----------------------------------|
| `created`         | `processing`, `cancelled`         |
| `processing`      | `ready_to_ship`, `cancelled`      |
| `ready_to_ship`   | `shipped`, `cancelled`            |
| `shipped`         | `delivered`, `cancelled`          |
| `delivered`       | `cancelled`                       |
| `cancelled`       | —                                 |

---

## Dependências

| Pacote    | Descrição                        |
|-----------|----------------------------------|
| Python    | 3.12                             |
| FastAPI   | Framework web assíncrono         |
| Uvicorn   | Servidor ASGI                    |
| Poetry    | Gerenciamento de dependências    |

---

## Observações

- O código do pedido é gerado sequencialmente: `ORD0000000`, `ORD0000001`, ...
- O cálculo da comissão é realizado pela função `calculate_comission` em `app/orders/domain/utils.py`.
- Todas as transições de status são validadas por `state_machine.py`.
- Os retornos da API são serializáveis via Pydantic ou `dict`.