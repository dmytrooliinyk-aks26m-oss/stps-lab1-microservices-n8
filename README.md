# stps-lab1-microservices-n8

Мікросервісна взаємодія на FastAPI та Docker Compose (варіант 8: порти `8008` та `9008`).

## UML-діаграма послідовності
```mermaid
sequenceDiagram
    autonumber
    actor Client as Клієнт / Newman
    participant Order as Order Service (:9008)
    participant Inv as Inventory Service (:8008)
    Client->>Order: POST /orders {item_id, quantity}
    Order->>Inv: POST /items/{item_id}/reserve {quantity}
    Inv-->>Order: 200 OK {remaining_stock}
    Order-->>Client: 201 Created {order_id, status: "confirmed"}
```

## Запуск
```bash
docker compose up --build -d
```
