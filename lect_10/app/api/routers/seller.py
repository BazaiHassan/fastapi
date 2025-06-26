from fastapi.params import Depends
from typing_extensions import Annotated
from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import oauth2_scheme

from app.api.dependencies import SellerServiceDep, SessionDep, get_access_token
from app.api.schemas.seller import SellerCreate, SellerRead
from app.database.models import Seller
from app.database.redis import add_jti_to_blacklist
from app.utils import decode_access_token


router = APIRouter(prefix="/seller", tags=["Seller"])


### Register a seller
@router.post("/signup", response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: SellerServiceDep):
    result = await service.add(seller)
    return result


### Login the seller
@router.post("/token")
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token":token,
        "type":"jwt"
    }


@router.get("/logout")
async def logout_seller(
    token_data:Annotated[dict, Depends(get_access_token)]
):
    await add_jti_to_blacklist(token_data["jti"])
    return {
        "details":"Successfully Logged out"
    }
