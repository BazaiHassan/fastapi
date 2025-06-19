# CRUD Operation

## 1. `PUT`
this method will update entire object

    ```bash
    @app.put("/profile")
    def update_profile(id: int, firstName: str, age:int, lastName:str) -> dict[str, Any]:
        s_database[id] = {"first name": firstName, "last name":lastName, "age":age}
        return {
            "data":s_database
        }
    ```


## 2. `PATCH`
this method will help us to update a record of an object

    ```bash
    @app.patch("/profile")
    def update_profile_key(id: int, body:dict[str, Any]):
        person = s_database[id]

        person.update(body)

        s_database[id] = person

        return {
            "data":s_database
        } 
    ```

## 2. `DELETE`
this method will be used for deleting an object

    ```bash
    @app.delete("/delete")
    def delete_person(id:int):
        s_database.pop(id)
        return {
            "message":f"The ID {id} is deleted",
            "data":s_database
        }
    ```
