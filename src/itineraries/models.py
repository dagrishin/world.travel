from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


from db.session import Base


class Itineraries(Base):
    __tablename__ = 'itineraries'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    user = relationship("Users", back_populates="itineraries")
    cities = relationship("Cities", secondary="itinerary_cities")
