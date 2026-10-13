
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

app = FastAPI(
    title="Zenstar024 Coffee Studio API",
    description="Coffee menu and custom order API",
    version="1.0.0"
)

MENU = {
    "Cappuccino": 320,
    "Caramel Latte": 390,
    "Americano": 250,
    "Mocha": 420,
    "Vanilla Latte": 380,
    "Cold Coffee": 350,
    "Espresso": 220,
    "Matcha Latte": 400,
}

SIZE_EXTRA = {"Small": 0, "Regular": 50, "Large": 100}

EXTRAS = {
    "Extra espresso": 80,
    "Vanilla": 50,
    "Caramel": 50,
    "Whipped cream": 60,
}

orders = []
next_order_id = 1


class CoffeeOrder(BaseModel):
    coffee: str
    size: Literal["Small", "Regular", "Large"] = "Regular"
    milk: Literal[
        "Whole milk", "Low-fat milk", "Oat milk",
        "Almond milk", "Soy milk", "No milk"
    ] = "Whole milk"
    sugar: Literal["0%", "25%", "50%", "75%", "100%"] = "50%"
    temperature: Literal["Hot", "Iced"] = "Hot"
    extras: list[str] = Field(default_factory=list)
    quantity: int = Field(default=1, ge=1, le=20)


@app.get("/")
def home():
    return {
        "app": "Zenstar024 Coffee Studio",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/menu")
def get_menu():
    return {
        "currency": "PKR",
        "note": "Illustrative demo prices, not official Starbucks prices.",
        "coffee": [
            {"name": name, "price": price}
            for name, price in MENU.items()
        ],
        "sizes": SIZE_EXTRA,
        "extras": EXTRAS
    }


@app.post("/orders")
def create_order(order: CoffeeOrder):
    global next_order_id

    if order.coffee not in MENU:
        raise HTTPException(400, "Coffee not found.")

    for extra in order.extras:
        if extra not in EXTRAS:
            raise HTTPException(400, f"Invalid extra: {extra}")

    unit_price = (
        MENU[order.coffee]
        + SIZE_EXTRA[order.size]
        + sum(EXTRAS[x] for x in order.extras)
    )

    total = unit_price * order.quantity

    result = {
        "order_id": next_order_id,
        **order.model_dump(),
        "unit_price": unit_price,
        "total": total,
        "currency": "PKR",
        "status": "Created"
    }

    orders.append(result)
    next_order_id += 1

    return result


@app.get("/orders")
def get_orders():
    return {"orders": orders, "count": len(orders)}


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            return order

    raise HTTPException(404, "Order not found.")
