# FastAPI with Pydantic: A Practical Guide

This guide explains how to use Pydantic with FastAPI to build robust APIs with data validation and automatic documentation.

## Table of Contents
1. [Introduction](#introduction)
2. [Setup](#setup)
3. [Basic Pydantic Model](#basic-pydantic-model)
4. [Using Models in FastAPI](#using-models-in-fastapi)
5. [Response Models](#response-models)
6. [Nested Models](#nested-models)
7. [Field Customization](#field-customization)
8. [Conclusion](#conclusion)

## Introduction

Pydantic is a data validation library that works seamlessly with FastAPI. It provides:
- Data validation
- Data conversion
- Automatic documentation
- Editor support

## Setup

First, install the required packages:

```bash
pip install fastapi pydantic uvicorn
```

Create a file `main.py` for your FastAPI application.

## Basic Pydantic Model

Let's start with a simple Pydantic model:

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
```

This model defines:
- Required `name` (string)
- Optional `description` (string or None)
- Required `price` (float)
- Optional `tax` (float or None)

## Using Models in FastAPI

Now let's use this model in a FastAPI endpoint:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
```

Key features:
- FastAPI automatically validates the request body against the `Item` model
- Invalid data returns a 422 Unprocessable Entity response
- The model appears in the automatic API documentation

## Response Models

You can specify a model for the response:

```python
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item
```

This ensures:
- Output data is validated against the model
- The documentation shows the response structure
- Sensitive data can be filtered (see next example)

Filtering response data:

```python
class UserIn(BaseModel):
    username: str
    password: str
    email: str

class UserOut(BaseModel):
    username: str
    email: str

@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user  # Password won't be included in the response
```

## Nested Models

Pydantic supports complex nested models:

```python
from typing import List

class Image(BaseModel):
    url: str
    name: str

class Product(BaseModel):
    name: str
    price: float
    images: List[Image] | None = None

@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    return {"product_id": product_id, **product.dict()}
```

Example valid payload:
```json
{
  "name": "Smartphone",
  "price": 599.99,
  "images": [
    {
      "url": "http://example.com/image1.jpg",
      "name": "Front view"
    },
    {
      "url": "http://example.com/image2.jpg",
      "name": "Back view"
    }
  ]
}
```

## Field Customization

You can add validation and metadata to fields:

```python
from pydantic import Field

class Item(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: str | None = Field(
        None, title="The description", max_length=300
    )
    price: float = Field(..., gt=0, description="Price must be positive")
    tax: float | None = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice item",
                "price": 35.4,
                "tax": 3.2,
            }
        }
```

This provides:
- Length validation for strings
- Value validation for numbers
- Enhanced documentation with examples
- Field descriptions in the schema

## Conclusion

Pydantic with FastAPI provides:
1. Automatic data validation
2. Type conversion
3. Comprehensive documentation
4. Editor support
5. Clean separation of concerns
