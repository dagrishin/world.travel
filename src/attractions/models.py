from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

from db.session import Base


class Attractions(Base):
    __tablename__ = 'attractions'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    city = relationship("Cities", back_populates="attractions")
    reviews = relationship(
        "Reviews",
        back_populates="attractions",
        primaryjoin="and_(Attractions.id == Reviews.review_id, Reviews.review_type==Attractions.__tablename__)"
    )
    content = relationship(
        "Content",
        back_populates="attractions",
        primaryjoin="and_(Attractions.id == Content.content_id, Content.content_type==Attractions.__tablename__)"
    )


class AttractionTags(Base):
    __tablename__ = 'attraction_tags'
    attraction_id = Column(Integer, ForeignKey('attractions.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)
    attraction = relationship("Attractions", back_populates="tags")
    tag = relationship("Tags")
