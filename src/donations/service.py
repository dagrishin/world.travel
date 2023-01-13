from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from src.donations.models import Donations
from src.dream_trips.models import DreamTrips
from src.service import BaseDAL


class DonationDAL(BaseDAL):
    """Data Access Layer for operating with donations"""

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Donations)

    async def create_donation(
            self, dream_id: int, user_id: int, amount: float
    ) -> Donations:
        dream = await DreamTrips.get_dream(dream_id)
        if not dream:
            raise ValueError("Dream does not exist")
        if amount > dream.max_donation:
            raise ValueError("Donation amount exceeds maximum allowed for this dream")
        new_donation = self._model(
            dream_id=dream_id,
            user_id=user_id,
            amount=amount
        )
        self.db_session.add(new_donation)
        try:
            await self.db_session.flush()
            await self.update_dream_donation_total(dream_id, amount)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create donation.")
        return new_donation

    async def update_dream_donation_total(self, dream_id: int, amount: float):
        dream = await DreamTrips.get_dream(dream_id)
        if not dream:
            raise ValueError("Dream does not exist")
        dream.donation_total += amount
        self.db_session.add(dream)
        try:
            await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Failed to update dream donation total.")

    async def get_donations_by_dream(self, dream_id: int) -> List[Donations]:
        query = select(self._model).where(self._model.dream_id == dream_id)
        queryset = await self.db_session.execute(query)
        donations = queryset.scalars().all()
        return donations

    async def get_donations_by_user(self, user_id: int) -> List[Donations]:
        query = select(self._model).where(self._model.user_id == user_id)
        queryset = await self.db_session.execute(query)
        donations = queryset.scalars().all()
        return donations
