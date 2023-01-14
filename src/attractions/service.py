from typing import List, Any, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.attractions import Attractions
from src.core import AttractionsTags, Tags
from src.service import BaseDAL
from src.travel import Cities
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

    async def get_query(self, name: Optional[str] = None, type: Optional[str] = None, city_id: Optional[int] = None,
                        tags: Optional[List[str]] = None):
        query = self.db_session.query(Attractions)
        if name:
            query = query.filter(Attractions.name.ilike(f"%{name}%"))
        if type:
            query = query.filter(Attractions.type == type)
        if city_id:
            query = query.filter(Attractions.city_id == city_id)
        if tags:
            query = query.filter(Attractions.tags.any(Tags.name.in_(tags)))
        return query

    # async def search(self, name: Optional[str] = None, type: Optional[str] = None, city_id: Optional[int] = None,
    #                  tags: Optional[List[str]] = None):
    #     query = await self.get_query(name, type, city_id, tags)
    #     return await query.all()

    async def search(self, name: str) -> List[Any]:
        query = select(self._model).where(self._model.name.ilike(f"%{name}%"))
        objs = await self.db_session.execute(query)
        return objs.scalars().all()

    async def filter_by_city(self, city_name: str) -> List[Any]:
        query = (
            select(self._model)
            .join(Cities)
            .where(Cities.name == city_name)
        )
        objs = await self.db_session.execute(query)
        return objs.scalars().all()

    async def get_by_tags(self, tags: List[str]) -> List[Any]:
        query = (
            select(self._model)
            .where(self._model.tags.in_(tags))
        )
        objs = await self.db_session.execute(query)
        return objs.scalars().all()

    async def get_by_name(self, name: str) -> List[Any]:
        query = select(self._model).where(self._model.name.ilike(f"%{name}%"))

        objs = await self.db_session.execute(query)
        return objs.scalars().all()
    async def get_by_type(self, type: str) -> List[Any]:
        query = select(self._model).where(self._model.type == type)
        objs = await self.db_session.execute(query)
        return objs.scalars().all()

    async def search(self, **kwargs: dict) -> List[Any]:
        query = select(self._model)
        for key, value in kwargs.items():
            column = getattr(self._model, key, None)
            if column:
                query = query.where(column.ilike(f"%{value}%"))
        objs = await self.db_session.execute(query)
        return objs.scalars().all()

    async def filter_by_tags(self, tags: List[str]) -> List[Any]:
        query = (
            select(self._model)
            .join(AttractionsTags)
            .join(Tags)
            .where(Tags.name.in_(tags))
        )
        objs = await self.db_session.execute(query)
        return objs.scalars().all()
