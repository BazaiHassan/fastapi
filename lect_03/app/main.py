from fastapi import FastAPI, status, HTTPException
from typing import Any

app = FastAPI()

books_db = {
    1: {"name": "book1", "genre": "genre1", "author": "author1", "price": "1000"},
    2: {"name": "book2", "genre": "genre2", "author": "author2", "price": "2000"},
}

@app.get("/book")
def get_book(id:int)->dict[str,Any]:
    if id not in books_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given ID dose not exist"
        )
    return books_db[id]


@app.post("/book")
def add_book(name:str, genre: str = "" , author: str = "", price:str = "")-> dict[str,str]:
    
    if name is None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="the name is mandatory"
        )
    return {
        "name":name
    }

@app.post("/author")
def add_author(data : dict[str,Any])-> dict[str,Any]:
    
    if data is None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="the name is mandatory"
        )
    return {
        "data":data
    }
