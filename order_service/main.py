"""Order Service (port 9008)."""

import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Order Service", version="1.0.0")
INVENTORY_URL = os.getenv("INVENTORY_SERVICE_URL", "http://inventory-service:8008")


class OrderCreate(BaseModel):
    """Order creation payload."""

    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


ORDERS_DB: list[dict] = []


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "order-service"}


@app.get("/orders")
def list_orders() -> list[dict]:
    """Return created orders."""
    return ORDERS_DB


@app.post("/orders", status_code=201)
async def create_order(order: OrderCreate) -> dict:
    """Create order after reserving stock in Inventory Service."""
    url = f"{INVENTORY_URL}/items/{order.item_id}/reserve"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(url, json={"quantity": order.quantity})
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Inventory unavailable: {exc}") from exc
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.json().get("detail", "Error"))
    data = resp.json()
    new_order = {"order_id": len(ORDERS_DB) + 1, "item_id": order.item_id, "quantity": order.quantity, "remaining_stock": data["remaining_stock"], "status": "confirmed"}
    ORDERS_DB.append(new_order)
    return new_order
