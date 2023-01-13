from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from src.core import Content, Tags
from src.core.schemas import ContentCreate, TagsCreate
from src.service import BaseDAL


class ContentDAL(BaseDAL):

    def __init__(self, db_session):
        super().__init__(db_session=db_session, model=Content)

    async def create_content(self, obj_in: ContentCreate):
        new_content = self._model(
            content_type=obj_in.content_type,
            content_id=obj_in.content_id,
            data=obj_in.data,
            image_urls=obj_in.image_urls,
        )
        self.db_session.add(new_content)
        try:
            await self.db_session.flush()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create content.")
        return new_content

    async def get_by_content_id_and_type(self, content_id: UUID, content_type: str) -> Optional[Content]:
        query = select(self._model).where(Content.content_id == content_id, Content.content_type == content_type)
        queryset = await self.db_session.execute(query)
        content_qs = queryset.first()
        if content_qs:
            (content,) = content_qs
            return content


class TagsDAL(BaseDAL):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Tags)

    async def create(self, obj_in: TagsCreate) -> Tags:
        new_tag = self._model(
            name=obj_in.name
        )
        self.db_session.add(new_tag)
        try:
            await self.db_session.flush()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create tag.")
        return new_tag
