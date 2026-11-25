"""Inventory Service (port 8008)."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Inventory Service", version="1.0.0")


class ReserveRequest(BaseModel):
    """Stock reservation payload."""

    quantity: int = Field(..., gt=0)


INVENTORY_DB: dict[int, dict] = {
    1: {"id": 1, "name": "LED Strip 24V", "stock": 50, "price": 320.0},
    2: {"id": 2, "name": "Power Supply 150W", "stock": 15, "price": 890.0},
    3: {"id": 3, "name": "Aluminum Profile", "stock": 5, "price": 210.0},
}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "inventory-service"}


@app.get("/items")
def get_items() -> list[dict]:
    """Return all inventory items."""
    return list(INVENTORY_DB.values())


@app.get("/items/{item_id}")
def get_item(item_id: int) -> dict:
    """Return item by ID."""
    item = INVENTORY_DB.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items/{item_id}/reserve")
def reserve_item(item_id: int, payload: ReserveRequest) -> dict:
    """Reserve stock for an item."""
    item = INVENTORY_DB.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item["stock"] < payload.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    item["stock"] -= payload.quantity
    return {"item_id": item_id, "reserved": payload.quantity, "remaining_stock": item["stock"]}
