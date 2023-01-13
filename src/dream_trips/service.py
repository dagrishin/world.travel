from typing import List, Any
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from src.dream_trips.models import DreamTrips, Likes
from src.service import BaseDAL


class DreamTripsDAL(BaseDAL):
    """Data Access Layer for operating dream"""

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session, model=DreamTrips)

    async def create_dream(
            self, obj_in
    ) -> DreamTrips:
        new_dream = self._model(
            name=obj_in.name,
            description=obj_in.description,
            target_amount=obj_in.target_amount,
            user_id=obj_in.user_id,
            current_amount=0
        )
        self.db_session.add(new_dream)
        try:
            await self.db_session.flush()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create dream.")
        return new_dream

    async def get_by_user_id(self, user_id: int) -> List[DreamTrips]:
        query = select(self._model).where(self._model.user_id == user_id)
        queryset = await self.db_session.execute(query)
        dreams = queryset.scalars().all()
        return dreams


class LikesDAL(BaseDAL):
    def init(self, db_session: AsyncSession):
        super().__init__(db_session, Likes)

    async def create(self, obj_in: dict) -> Any:
        new_obj = self._model(**obj_in)
        self.db_session.add(new_obj)
        try:
            await self.db_session.flush()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create object.")
        return new_obj

    async def delete(self, user_id: UUID, dream_trip_id: int):
        query = sqlalchemy_delete(self._model).where(self._model.user_id == user_id,
                                                     self._model.dream_trip_id == dream_trip_id)
        await self.db_session.execute(query)
        try:
            await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete object.")
        return True
