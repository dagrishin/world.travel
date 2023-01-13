import uuid

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.session import Base
from src.tracks import Track, Place


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean(), default=False)

    reviews = relationship("Reviews", back_populates="user")
    user_travel_experiences = relationship("UserTravelExperiences", back_populates="user")
    bookings = relationship("Booking", back_populates="user")
    tracks = relationship("Track", back_populates="user")
    places = relationship("Place", back_populates="user")

    content = relationship(
        "Content",
        back_populates="user",
        primaryjoin="and_(User.id == foreign(Content.content_id), Content.content_type=='users')"
    )
