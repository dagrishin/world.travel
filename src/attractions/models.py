import uuid

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from db.session import Base
from src.core import Content, Tags
from src.travel_posts import Reviews


class Attractions(Base):
    __tablename__ = 'attractions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    city = relationship("Cities", back_populates="attractions")
    places = relationship("Place", back_populates="attraction")
    tags = relationship("Tags", secondary="attractions_tags")
    reviews = relationship(
        "Reviews",
        back_populates="attraction",
        primaryjoin="and_(Attractions.id == foreign(Reviews.review_id), Reviews.review_type=='attractions')",
    )
    content = relationship(
        "Content",
        back_populates="attraction",
        primaryjoin="and_(Attractions.id == foreign(Content.content_id), Content.content_type=='attractions')"
    )
