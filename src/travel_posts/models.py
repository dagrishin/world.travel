from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from db.session import Base


class UserTravelExperiences(Base):
    __tablename__ = 'user_travel_experiences'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    location = Column(String(255), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    country = relationship("Countries", back_populates="travel_experiences")
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    user = relationship("Users", back_populates="travel_experiences")

    reviews = relationship(
        "Reviews",
        back_populates="user_travel_experience",
        primaryjoin="and_(UserTravelExperiences.id == Reviews.review_id, Reviews.review_type==UserTravelExperiences.__tablename__)"
    )
    content = relationship(
        "Content",
        back_populates="user_travel_experience",
        primaryjoin="and_(UserTravelExperiences.id == Content.content_id, Content.content_type==UserTravelExperiences.__tablename__)"
    )


class Reviews(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    user = relationship("Users", back_populates="reviews")
    review_type = Column(String, nullable=False)
    review_id = Column(Integer, nullable=False)
    data = Column(String, nullable=False)
    image_urls = Column(JSON, nullable=True)
    attraction = relationship("Attractions", back_populates="reviews")
    hotel = relationship("Hotels", back_populates="reviews")
    restaurant = relationship("Restaurants", back_populates="reviews")
    user_travel_experience = relationship("UserTravelExperiences", back_populates="reviews")

    content = relationship(
        "Content",
        back_populates="reviews",
        primaryjoin="and_(Reviews.id == Content.content_id, Content.content_type==Reviews.__tablename__)"
    )
