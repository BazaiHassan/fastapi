from fastapi import FastAPI, HTTPException, status
from app.database import Database
from app.schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate


app = FastAPI()
db = Database()

@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id:int):
    shipment = db.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Give id doesn't exist!"
        )
    return shipment

@app.get("/shipments", response_model=list[ShipmentRead])
def get_all_shipments():
    shipments = db.get_all()
    if not shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "No shipments found!"
        )
    return shipments


@app.post("/shipment", response_model=None)
def submit_shipment(shipment:ShipmentCreate):
    new_id = db.create(shipment)
    return {"id":new_id}

@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id:int, shipment:ShipmentUpdate):
    shipment = db.update(id=id, shipment=shipment)
    
    return shipment

@app.delete("/shipment", response_model=dict[str, str])
def delete_shipment(id:int):
    db.delete(id)
    return {"message":"Shipment deleted successfully!"}