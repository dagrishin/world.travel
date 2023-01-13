from typing import Any, List

from fastapi import HTTPException
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status


class BaseDAL:
    def __init__(self, db_session: AsyncSession, model):
        self.db_session = db_session
        self._model = model

    async def create(self, obj_in: dict) -> Any:
        new_obj = self._model(**obj_in)
        self.db_session.add(new_obj)
        try:
            await self.db_session.flush()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create object.")
        return new_obj

    async def update(self, id: int, update_data: dict):
        query = (
            sqlalchemy_update(self._model)
            .where(self._model.id == id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        await self.db_session.execute(query)
        try:
            await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update object.")

    async def get(self, id: int) -> Any:
        query = select(self._model).where(self._model.id == id)
        queryset = await self.db_session.execute(query)
        obj_qs = queryset.first()
        if obj_qs:
            (obj, ) = obj_qs
            return obj

    async def get_all(self) -> List[Any]:
        query = select(self._model)
        objs = await self.db_session.execute(query)
        return objs.scalars().all()

    async def delete(self, id: int):
        query = sqlalchemy_delete(self._model).where(self._model.id == id)
        await self.db_session.execute(query)
        try:
            await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete object.")
        return True
