import uuid

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.session import Base


class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="bookings")
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    hotel = relationship("Hotels", back_populates="bookings")
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    restaurant = relationship("Restaurants", back_populates="bookings")
