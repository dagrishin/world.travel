from typing import List, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.attractions import Attractions
from src.core import AttractionsTags, Tags
from src.service import BaseDAL
from src.travel_posts import Reviews


class AttractionsDAL(BaseDAL):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Attractions)

    async def get_by_city_id(self, city_id: int) -> List[Any]:
        query = select(self._model).where(self._model.city_id == city_id)
        objs = await self.db_session.execute(query)
        return objs.scalars().all()

    async def get_by_type(self, attraction_type: str) -> List[Any]:
        query = select(self._model).where(self._model.type == attraction_type)
        objs = await self.db_session.execute(query)
        return objs.scalars().all()

    async def get_by_name(self, attraction_name: str) -> List[Any]:
        query = select(self._model).where(self._model.name == attraction_name)
        objs = await self.db_session.execute(query)
        return objs.scalars().all()

    async def get_by_tag(self, tag_name: str) -> List[Any]:
        query = select(self._model).join(AttractionsTags).join(Tags).where(Tags.name == tag_name)
        objs = await self.db_session.execute(query)
        return objs.scalars().all()

    async def get_reviews_by_attraction_id(self, attraction_id: UUID) -> List[Any]:
        query = select(Reviews).join(self._model).where(self._model.id == attraction_id)
        objs = await self.db_session.execute(query)
        return objs.scalars().all()
