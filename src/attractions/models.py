from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

from db.session import Base
from src.core import Content, Tags
from src.travel_posts import Reviews


class Attractions(Base):
    __tablename__ = 'attractions'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    city = relationship("Cities", back_populates="attractions")
    places = relationship("Place", back_populates="attraction")
    # tags = relationship("Tags", back_populates="attractions_tags")
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


# class AttractionTags(Base):
#     __tablename__ = 'attraction_tags'
#     attraction_id = Column(Integer, ForeignKey('attractions.id'), primary_key=True)
#     tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)
#     attraction = relationship("Attractions", back_populates="attraction_tags")
#     tag = relationship("Tags", back_populates="attraction_tags")
