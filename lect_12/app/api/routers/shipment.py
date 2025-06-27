from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import SellerDep, ShipmentServiceDep
from app.api.schemas.shipment import ShipmentCreate, ShipmentUpdate, ShipmentRead


router = APIRouter(prefix="/shipment", tags=["Shipment"])


@router.get("/", response_model=ShipmentRead)
async def get_shipment(id: str, service: ShipmentServiceDep, _: SellerDep):
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id does not exist!"
        )

    return shipment


@router.post("/", response_model=ShipmentRead)
async def submit_shipment(
    shipment: ShipmentCreate, service: ShipmentServiceDep, seller: SellerDep
):
    return await service.add(shipment, seller)


@router.patch("/", response_model=ShipmentRead)
async def update_shipment(
    id: str, shipment_update: ShipmentUpdate, service: ShipmentServiceDep, _: SellerDep
):
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update.",
        )

    return await service.update(id, update)


@router.delete("/")
async def delete_shipment(id: str, service: ShipmentServiceDep, _: SellerDep):
    await service.delete(id)
    return {"detail": f"Shipment with id #{id} is deleted!"}
