from datetime import datetime, timedelta
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from fastapi import HTTPException, status

from app.config import security_settings
from app.api.schemas.seller import SellerCreate
from app.database.models import Seller
from app.utils import generate_access_token

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, credentials: SellerCreate) -> Seller:
        seller = Seller(
            **credentials.model_dump(exclude={"password"}),
            password_hash=password_context.hash(credentials.password),
        )

        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)
        return seller

    async def token(self, email, password) -> str:
        # Validate the credentials
        result = await self.session.execute(select(Seller).where(Seller.email == email))

        seller = result.scalar()

        if seller is None or not password_context.verify(
            password,
            seller.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or Password is incorrect",
            )
        
        token = generate_access_token(
            data={
                "user": {
                    "name": seller.name,
                    "id": str(seller.id),
                }
            }
        )

        return token
