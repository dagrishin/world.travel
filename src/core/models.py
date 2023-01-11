from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship

from db.session import Base


class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class Content(Base):
    __tablename__ = 'content'
    id = Column(Integer, primary_key=True)
    content_type = Column(String, nullable=False)
    content_id = Column(Integer, nullable=False)
    data = Column(String, nullable=False)
    image_urls = Column(JSON, nullable=True)
    attraction = relationship("Attractions", back_populates="content")
    hotel = relationship("Hotels", back_populates="content")
    restaurant = relationship("Restaurants", back_populates="content")
    user_travel_experience = relationship("UserTravelExperiences", back_populates="content")
    review = relationship("Reviews", back_populates="content")
