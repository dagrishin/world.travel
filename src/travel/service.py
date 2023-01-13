from typing import Any, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.service import BaseDAL
from src.travel import Countries, Cities, Address, Hotels, Weather, Restaurants


class CountriesDAL(BaseDAL):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Countries)

    async def get_by_name(self, name: str) -> Any:
        query = select(self._model).where(self._model.name == name)
        queryset = await self.db_session.execute(query)
        obj_qs = queryset.first()
        if obj_qs:
            (obj,) = obj_qs
            return obj

    async def get_by_continent(self, continent: str) -> List[Any]:
        query = select(self._model).where(self._model.continent == continent)
        queryset = await self.db_session.execute(query)
        return queryset.scalars().all()


class CitiesDAL(BaseDAL):
    def __init__(self, db_session):
        super().__init__(db_session, model=Cities)

    async def get_by_name(self, name: str) -> Any:
        query = select(self._model).where(self._model.name == name)
        queryset = await self.db_session.execute(query)
        obj_qs = queryset.first()
        if obj_qs:
            (obj,) = obj_qs
            return obj

    async def get_by_population(self, population: int) -> List[Any]:
        query = select(self._model).where(self._model.population == population)
        queryset = await self.db_session.execute(query)
        return queryset.scalars().all()


class AddressDAL(BaseDAL):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Address)

    async def get_by_zipcode(self, zipcode: str) -> List[Address]:
        query = select(self._model).where(self._model.zipcode == zipcode)
        objs = await self.db_session.execute(query)
        return objs.scalars().all()


class HotelsDAL(BaseDAL):
    def __init__(self, db_session):
        super().__init__(db_session, Hotels)

    async def get_by_rating(self, rating: float) -> List[Hotels]:
        query = select(self._model).where(self._model.rating == rating)
        objs = await self.db_session.execute(query)
        return objs.scalars().all()

    async def get_by_name(self, name: str) -> List[Hotels]:
        query = select(self._model).where(Hotels.name.ilike(f"%{name}%"))
        objs = await self.db_session.execute(query)
        return objs.scalars().all()


class RestaurantsDAL(BaseDAL):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Restaurants)

    async def get_by_name(self, name: str) -> Any:
        query = select(self._model).where(self._model.name == name)
        queryset = await self.db_session.execute(query)
        obj_qs = queryset.first()
        if obj_qs:
            (obj,) = obj_qs
            return obj

    async def get_by_rating(self, rating: float) -> Any:
        query = select(self._model).where(self._model.rating == rating)
        queryset = await self.db_session.execute(query)
        obj_qs = queryset.first()
        if obj_qs:
            (obj,) = obj_qs
            return obj

    async def get_by_city(self, city: str) -> Any:
        query = select(self._model).where(self._model.city == city)
        queryset = await self.db_session.execute(query)
        obj_qs = queryset.first()
        if obj_qs:
            (obj,) = obj_qs
            return obj


class WeatherDAL(BaseDAL):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Weather)

    async def get_by_city_id(self, city_id: int) -> List[Any]:
        query = select(self._model).where(self._model.city_id == city_id)
        objs = await self.db_session.execute(query)
        return objs.scalars().all()

    async def get_by_date(self, date: str) -> List[Any]:
        query = select(self._model).where(self._model.date == date)
        objs = await self.db_session.execute(query)
        return objs.scalars().all()

    async def get_by_condition(self, condition: str) -> List[Any]:
        query = select(self._model).where(self._model.condition == condition)
        objs = await self.db_session.execute(query)
        return objs.scalars().all()
