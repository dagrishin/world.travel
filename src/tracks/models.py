import uuid

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


from db.session import Base


class Track(Base):
    __tablename__ = 'tracks'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="tracks")
    name = Column(String)
    places = relationship("Place", back_populates="track")


class Place(Base):
    __tablename__ = 'places'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    type = Column(String)
    user_id = Column(UUID, ForeignKey('users.id'))
    user = relationship("User", back_populates="places")
    address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
    address = relationship("Address", back_populates="places")
    attraction_id = Column(Integer, ForeignKey('attractions.id'), nullable=False)
    attraction = relationship("Attractions", back_populates="places")
    hotels_id = Column(Integer, ForeignKey('hotels.id'), nullable=False)
    hotel = relationship("Hotels", back_populates="places")
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    restaurant = relationship("Restaurants", back_populates="places")
    track_id = Column(Integer, ForeignKey('tracks.id'), nullable=False)
    track = relationship("Track", back_populates="places")


# class TrackPlaces(Base):
#     __tablename__ = 'track_places'
#     track_id = Column(Integer, ForeignKey('tracks.id'), primary_key=True)
#     place_id = Column(Integer, ForeignKey('places.id'), primary_key=True)
