import re
import uuid
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class ShowUser(TunedModel):
    id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class UserUpdate(TunedModel):
    name: str = None
    surname: str = None
    email: EmailStr = None
    password: Optional[str] = None


class UserCreate(BaseModel):
    name: str
    surname: str
    password: str
    email: EmailStr

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    subject: str
    token_type: str
    exp: int


class Msg(BaseModel):
    msg: str
