from typing import Optional

from fastapi import HTTPException
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from src.auth.authentication import get_password_hash, verify_password
from src.auth.models import User
from src.auth.schemas import UserCreate


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self._model = User

    async def create_user(
            self, obj_in: UserCreate
    ) -> User:
        new_user = self._model(
            name=obj_in.name,
            surname=obj_in.surname,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
        )
        self.db_session.add(new_user)
        try:
            await self.db_session.flush()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user.")
        return new_user

    async def update(self, id, update_data):
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
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
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update user.")

    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(self._model).where(User.email == email)
        queryset = await self.db_session.execute(query)
        user_qs = queryset.first()
        if user_qs:
            (user,) = user_qs
            return user

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
        except Exception as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete user.")
        return True

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def is_active(self, user: User) -> bool:
        return user.is_active

    async def is_superuser(self, user: User) -> bool:
        return user.is_superuser
