from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


from db.session import Base


class Track(Base):
    __tablename__ = 'tracks'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    user = relationship("Users", back_populates="tracks")
    name = Column(String)
    places = relationship("Place", secondary="track_places")


class Place(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    user_id = Column(UUID, ForeignKey('users.id'))
    user = relationship("User", back_populates="place")
    address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
    address = relationship("Address", back_populates="place")
    attractions_id = Column(Integer, ForeignKey('attractions.id'), nullable=False)
    attractions = relationship("Attractions", back_populates="place")
    hotels_id = Column(Integer, ForeignKey('hotels.id'), nullable=False)
    hotels = relationship("hotels", back_populates="place")
    restaurants_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    restaurants = relationship("Restaurants", back_populates="place")


class TrackPlaces(Base):
    __tablename__ = 'track_places'
    track_id = Column(Integer, ForeignKey('tracks.id'), primary_key=True)
    place_id = Column(Integer, ForeignKey('places.id'), primary_key=True)
