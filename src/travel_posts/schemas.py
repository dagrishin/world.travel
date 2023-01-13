from typing import Any, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core import Content
from src.service import BaseDAL
from src.travel_posts import UserTravelExperiences, Reviews


class UserTravelExperiencesDAL(BaseDAL):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, UserTravelExperiences)

    async def get_by_user(self, user_id: UUID) -> List[Any]:
        query = select(self._model).where(self._model.user_id == user_id)
        objs = await self.db_session.execute(query)
        return objs.scalars().all()

    async def get_reviews_by_user_travel_experience(self, user_travel_experience_id: UUID) -> List[Any]:
        query = select(Reviews).where(Reviews.review_id == user_travel_experience_id,
                                      Reviews.review_type == 'user_travel_experiences')
        objs = await self.db_session.execute(query)
        return objs.scalars().all()

    async def get_content_by_user_travel_experience(self, user_travel_experience_id: UUID) -> List[Any]:
        query = select(Content).where(Content.content_id == user_travel_experience_id,
                                      Content.content_type == 'user_travel_experiences')
        objs = await self.db_session.execute(query)
        return objs.scalars().all()
