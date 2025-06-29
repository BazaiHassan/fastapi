from pydantic import BaseModel, Field
from enum import Enum


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"

class BaseShipment(BaseModel):
    content:str
    weight:float = Field(le=25)

class ShipmentRead(BaseShipment):
    status : ShipmentStatus

class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    content:str|None = Field(default=None)
    weight:float| None = Field(default=None,le=25)
    status : ShipmentStatus