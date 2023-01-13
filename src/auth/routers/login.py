from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.session import get_async_db
from src.auth.authentication import create_access_token, create_refresh_token, verify_password_reset_token, \
    get_password_hash, generate_password_reset_token
from src.auth.dependencies import get_refresh_token_data
from src.auth.exceptions import send_reset_password_email
from src.auth.schemas import Token, TokenPayload, Msg
from src.auth.service import UserDAL
from src.config import settings

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_access_token(
        db: AsyncSession = Depends(get_async_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.authenticate(
                email=form_data.username, password=form_data.password
            )
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
            elif not user_dal.is_active(user):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
            access_token_expires = timedelta(
                minutes=settings.TOKEN_EXPIRE_MINUTES[settings.ACCESS_TOKEN_STR]
            )
            refresh_token_expires = timedelta(
                minutes=settings.TOKEN_EXPIRE_MINUTES[settings.REFRESH_TOKEN_STR]
            )
            return {
                "access_token": await create_access_token(
                    {"sub": form_data.username, "subject": str(user.id), "token_type": settings.ACCESS_TOKEN_STR},
                    expires_delta=access_token_expires,
                ),
                "refresh_token": await create_refresh_token(
                    {"sub": form_data.username, "subject": str(user.id), "token_type": settings.REFRESH_TOKEN_STR},
                    expires_delta=refresh_token_expires,
                ),
                "token_type": "bearer",
            }


@router.post("/token/refresh")
async def refresh_access_token(
        refresh_token: str,
        db: AsyncSession = Depends(get_async_db),
        refresh_token_data: TokenPayload = Depends(get_refresh_token_data),
) -> Any:
    user_id: str = refresh_token_data.subject
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get(
                id=user_id
            )
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            elif not user_dal.is_active(user):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
            access_token_expires = timedelta(
                minutes=settings.TOKEN_EXPIRE_MINUTES[settings.ACCESS_TOKEN_STR]
            )
            refresh_token_expires = timedelta(
                minutes=settings.TOKEN_EXPIRE_MINUTES[settings.REFRESH_TOKEN_STR]
            )
            return {
                "access_token": await create_access_token(
                    {"sub": refresh_token_data.sub, "subject": str(user_id), "token_type": settings.ACCESS_TOKEN_STR},
                    expires_delta=access_token_expires,
                ),
                "refresh_token": await create_refresh_token(
                    {"sub": refresh_token_data.sub, "subject": str(user_id), "token_type": settings.REFRESH_TOKEN_STR},
                    expires_delta=refresh_token_expires,
                ),
                "token_type": "bearer",
            }


@router.post("/password-recovery/{email}", response_model=Msg)
async def recover_password(email: str, db: AsyncSession = Depends(get_async_db)) -> Any:
    """
    Password Recovery
    """
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_by_email(email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = await generate_password_reset_token(email=email)
    await send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=Msg)
async def reset_password(
        token: str = Body(...),
        new_password: str = Body(...),
        db: AsyncSession = Depends(get_async_db),
) -> Any:
    """
    Reset password
    """
    email = await verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_by_email(email=email)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="The user with this username does not exist in the system.",
                )
            elif not user_dal.is_active(user):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
            hashed_password = get_password_hash(new_password)
            user.hashed_password = hashed_password
            session.add(user)
            await session.flush()
            return {"msg": "Password updated successfully"}
