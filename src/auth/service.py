from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.auth.models import User


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self._model = User

    async def create_user(
            self, name: str, surname: str, email: str
    ) -> User:
        new_user = self._model(
            name=name,
            surname=surname,
            email=email,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def update(self, id, **kwargs):
        query = (
            sqlalchemy_update(self._model)
            .where(self._model.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await self.db_session.execute(query)

        try:
            await self.db_session.commit()
        except Exception:
            await self.db_session.rollback()
            raise

    async def get(self, id):
        query = select(self._model).where(User.id == id)
        queryset = await self.db_session.execute(query)
        (user,) = queryset.first()
        return user

    async def get_all(self):
        query = select(self._model)
        users = await self.db_session.execute(query)
        users = users.scalars().all()
        return users

    async def delete(self, id):
        query = sqlalchemy_delete(self._model).where(self._model.id == id)
        await self.db_session.execute(query)
        try:
            await self.db_session.commit()
        except Exception:
            await self.db_session.rollback()
            raise
        return True
