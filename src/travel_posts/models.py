import uuid

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.session import Base


class UserTravelExperiences(Base):
    __tablename__ = 'user_travel_experiences'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    location = Column(String(255), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    country = relationship("Countries", back_populates="user_travel_experiences")
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    city = relationship("Cities", back_populates="user_travel_experiences")
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="user_travel_experiences")

    reviews = relationship(
        "Reviews",
        back_populates="user_travel_experience",
        primaryjoin="and_(UserTravelExperiences.id == foreign(Reviews.review_id), Reviews.review_type=='user_travel_experiences')",
    )
    content = relationship(
        "Content",
        back_populates="user_travel_experience",
        primaryjoin="and_(UserTravelExperiences.id == foreign(Content.content_id), Content.content_type=='user_travel_experiences')"
    )


class Reviews(Base):
    __tablename__ = 'reviews'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="reviews")
    review_type = Column(String, nullable=False)
    review_id = Column(UUID, nullable=False)
    data = Column(String, nullable=False)
    image_urls = Column(JSON, nullable=True)

    content = relationship(
        "Content",
        back_populates="review",
        primaryjoin="and_(Reviews.id == foreign(Content.content_id), Content.content_type=='reviews')"
    )

    user_travel_experience = relationship(
        "UserTravelExperiences",
        primaryjoin="and_(UserTravelExperiences.id == foreign(Reviews.review_id), Reviews.review_type=='user_travel_experiences')",
        back_populates="reviews"
    )

    attraction = relationship(
        "Attractions",
        back_populates="reviews",
        primaryjoin="and_(Attractions.id == foreign(Reviews.review_id), Reviews.review_type=='attractions')",
    )

    hotel = relationship(
        "Hotels",
        back_populates="reviews",
        primaryjoin="and_(Hotels.id == foreign(Reviews.review_id), Reviews.review_type=='hotels')",
    )

    restaurant = relationship(
        "Restaurants",
        back_populates="reviews",
        primaryjoin="and_(Restaurants.id == foreign(Reviews.review_id), Reviews.review_type=='restaurants')",
    )
