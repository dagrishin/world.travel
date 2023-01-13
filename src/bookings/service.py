from typing import List
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from src.bookings import Booking
from src.bookings.schemas import BookingCreate
from src.service import BaseDAL


class BookingDAL(BaseDAL):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session, model=Booking)

    async def create_booking(self, obj_in: BookingCreate):
        new_booking = self._model(
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            user_id=obj_in.user_id,
            hotel_id=obj_in.hotel_id,
            restaurant_id=obj_in.restaurant_id
        )
        self.db_session.add(new_booking)
        try:
            await self.db_session.flush()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create booking.")
        return new_booking

    async def get_by_user_id(self, user_id: UUID) -> List[Booking]:
        query = select(self._model).where(Booking.user_id == user_id)
        queryset = await self.db_session.execute(query)
        bookings = queryset.scalars().all()
        return bookings
