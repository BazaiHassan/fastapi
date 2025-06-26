from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from app.database.redis import is_jti_blacklisted
from app.database.session import get_session
from app.services.shipment import ShipmentService
from app.services.seller import SellerService
from app.utils import decode_access_token
from app.core.security import oauth2_scheme
from app.database.models import Seller
SessionDep = Annotated[AsyncSession, Depends(get_session)]

# Dependency for ShipmentService
def get_shipment_service(session: SessionDep):
    return ShipmentService(session=session)

# Dependency for SellerService
def get_seller_service(session: SessionDep):
    return SellerService(session=session)

# Access token data dependency
async def get_access_token(token: Annotated[str, Depends(oauth2_scheme)])->dict:
    data = decode_access_token(token)
    
    if data is None or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or Expiration access token",
        )
    return data


async def get_current_seller(token_data:Annotated[dict, Depends(get_access_token)], session: SessionDep):
    user_id = token_data.get("user", {}).get("id")
    # user_id = token_data["user"]["id"]
    user = session.get(Seller, user_id)
    return user



SellerDep = Annotated[Seller, Depends(get_current_seller)]
ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]