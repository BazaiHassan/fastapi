from datetime import datetime, timedelta
from typing import Optional
import pytz

from app.api.schemas.shipment import ShipmentCreate
from app.database.models import Seller, Shipment, ShipmentStatus
from sqlalchemy.ext.asyncio import AsyncSession


class ShipmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _normalize_datetime(self, dt: Optional[datetime]) -> Optional[datetime]:
        """Convert timezone-aware datetime to naive datetime for database storage."""
        if dt is None:
            return None
        
        if dt.tzinfo is not None:
            # Convert to UTC if it has timezone info, then make it naive
            if dt.tzinfo != pytz.UTC:
                dt = dt.astimezone(pytz.UTC)
            return dt.replace(tzinfo=None)
        
        return dt

    def _get_current_utc_naive(self) -> datetime:
        """Get current UTC time as a naive datetime."""
        return datetime.utcnow()

    async def get(self, id: str):
        return await self.session.get(Shipment, id)

    async def add(self, shipment_create: ShipmentCreate, seller: Seller) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=self._get_current_utc_naive() + timedelta(days=3),
            seller_id=seller.id,
        )
        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)

        return new_shipment

    async def update(self, id: str, shipment_update: dict) -> Shipment:
        shipment = await self.get(id)
        
        # Normalize any datetime fields in the update dict
        normalized_update = {}
        for key, value in shipment_update.items():
            if isinstance(value, datetime):
                normalized_update[key] = self._normalize_datetime(value)
            else:
                normalized_update[key] = value
        
        shipment.sqlmodel_update(normalized_update)

        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)

        return shipment

    async def delete(self, id: str) -> None:
        shipment = await self.get(id)
        await self.session.delete(shipment)
        await self.session.commit()