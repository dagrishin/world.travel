import uuid

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


from db.session import Base


class DreamTrips(Base):
    __tablename__ = 'dream_trips'
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="dream_trips")
    destination = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    goal = Column(String, nullable=False)
    collected_funds = Column(Float, nullable=False)
    goal_funds = Column(Float, nullable=False)
    deadline = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    likes = relationship("Likes", back_populates="dream_trip")
    donations = relationship("Donations", back_populates="dream_trip")


class Likes(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    dream_trip_id = Column(Integer, ForeignKey('dream_trips.id'), nullable=False)
    dream_trip = relationship("DreamTrips", back_populates="likes")