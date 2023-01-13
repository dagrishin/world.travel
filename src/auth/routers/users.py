from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.session import get_async_db
from src.auth import User
from src.auth.dependencies import get_current_active_superuser, get_current_active_user
from src.auth.utils import send_new_account_email
from src.auth.schemas import ShowUser, UserCreate, UserUpdate
from src.auth.service import UserDAL
from src.config import settings

router = APIRouter()


@router.post("/", response_model=ShowUser)
async def create_user(
        *,
        user_in: UserCreate, db: AsyncSession = Depends(get_async_db),
        # current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_by_email(email=user_in.email)
            if user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The user with this username already exists in the system.",
                )
            user = await user_dal.create_user(user_in)
            if settings.EMAILS_ENABLED and user_in.email:
                await send_new_account_email(
                    email_to=user_in.email, username=user_in.email, password=user_in.password
                )
            return ShowUser(
                id=user.id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active,
            )


@router.put("/me", response_model=ShowUser)
async def update_user_me(
        *,
        db: AsyncSession = Depends(get_async_db),
        password: str = Body(None),
        name: str = Body(None),
        surname: str = Body(None),
        email: EmailStr = Body(None),
        current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if name is not None:
        user_in.name = name
    if surname is not None:
        user_in.surname = surname
    if email is not None:
        user_in.email = email
    update_data = user_in.dict(exclude_unset=True)
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            await user_dal.update(id=current_user.id, update_data=update_data)
    update_data.update(id=current_user.id, is_active=current_user.is_active)
    return update_data


@router.get("/me", response_model=ShowUser)
def read_user_me(
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.get("/{user_id}", response_model=ShowUser)
async def read_user_by_id(
        user_id: str,
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_async_db),
) -> Any:
    """
    Get a specific user by id.
    """
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get(id=user_id)
    return user
