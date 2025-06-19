# FastAPI Lecture 3

## 1.Query Parameter

here when we want to send request with query parameter, the only thing that we must do is give the parameter to function signature.
`/book?id=1`

    ```bash
    @app.get("/book")
    def get_book(id:int)->dict[str,Any]:
        if id not in books_db:
            return {
                "detail":"Given id doesn't exist"
            }
        return books_db[id]
    ```
## 2.HTTP Exception
here when the getting results are not successful the HTTP code must be different. The default value is 200.

    ```bash
    @app.get("/book")
    def get_book(id:int)->dict[str,Any]:
        if id not in books_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Given ID dose not exist"
            )
        return books_db[id]
    ```

## 3.Request Body
Here when we want to use post method to send some value to server, we can do exactly like query parameters in `GET Method`.
> If you want to use `name:str|None=None` parameter initialization you must have python version `10.0+`

    ```bash
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
        ```