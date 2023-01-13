from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlmodel.ext.asyncio.session import AsyncSession

from db.session import get_async_db
from src.auth import User
from src.auth.authentication import ALGORITHM
from src.auth.schemas import TokenPayload
from src.auth.service import UserDAL
from src.config import settings

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)


async def get_user_from_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        expires_at = datetime.fromtimestamp(token_data.exp)
        if expires_at < datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired")
        return token_data
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(db: AsyncSession = Depends(get_async_db), token: str = Depends(reusable_oauth2)) -> User:
    token_data = await get_user_from_token(token)
    if token_data.token_type != settings.ACCESS_TOKEN_STR:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get(id=token_data.subject)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return user


async def get_current_active_user(
        current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
        current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="The user doesn't have enough privileges"
        )
    return current_user


async def get_refresh_token_data(refresh_token: str) -> TokenPayload:
    token_data = await get_user_from_token(refresh_token)
    if token_data.token_type != settings.REFRESH_TOKEN_STR:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    return token_data
