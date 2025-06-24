from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database.session import get_session
from app.services.shipment import ShipmentService
from app.services.seller import SellerService

SessionDep = Annotated[AsyncSession, Depends(get_session)]

# Dependency for ShipmentService
def get_shipment_service(session: SessionDep):
    return ShipmentService(session=session)

ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]


# Dependency for SellerService
def get_seller_service(session: SessionDep):
    return SellerService(session=session)

SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]