from typing import List, Any
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from src.service import BaseDAL
from src.tracks import Track, Place
from src.tracks.schemas import TrackCreate


class TrackDAL(BaseDAL):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Track)

    async def create_track(self, obj_in: TrackCreate) -> Track:
        new_track = self._model(
            title=obj_in.title,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            user_id=obj_in.user_id,
        )
        self.db_session.add(new_track)
        try:
            await self.db_session.flush()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create track.")
        return new_track

    async def get_track_by_user(self, user_id: UUID) -> List[Track]:
        query = select(self._model).where(Track.user_id == user_id)
        objs = await self.db_session.execute(query)
        return objs.scalars().all()


class PlaceDAL(BaseDAL):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Place)

    async def get_by_user_id(self, user_id: UUID) -> List[Any]:
        query = select(self._model).where(self._model.user_id == user_id)
        queryset = await self.db_session.execute(query)
        return queryset.scalars().all()
