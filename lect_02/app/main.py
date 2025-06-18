from fastapi import FastAPI
from typing import Any

app = FastAPI()


@app.get("/product/latest")
def get_latest_product():
    return {
        "id": 1,
        "name": "Latest Product",
        "price": 29.99,
        "description": "This is the latest product description.",
    }


@app.get("/product/{id}")
def get_product(id: int) -> dict[str, Any]:
    return {
        "id": id,
        "name": "Sample Product",
        "price": 19.99,
        "description": "This is a sample product description.",
    }
