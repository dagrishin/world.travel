from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.service import BaseDAL
from src.travel_posts import Reviews, UserTravelExperiences


class UserTravelExperiencesDAL(BaseDAL):
    def __init__(self, db_session):
        super().__init__(db_session, UserTravelExperiences)


class ReviewsDAL(BaseDAL):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Reviews)

    async def get_reviews_by_user_id(self, user_id: UUID) -> List[Reviews]:
        query = select(self._model).where(self._model.user_id == user_id)
        reviews = await self.db_session.execute(query)
        return reviews.scalars().all()

    async def get_reviews_by_review_type(self, review_type: str, review_id: UUID) -> List[Reviews]:
        query = select(self._model).where(
            self._model.review_type == review_type, self._model.review_id == review_id)
        reviews = await self.db_session.execute(query)
        return reviews.scalars().all()
