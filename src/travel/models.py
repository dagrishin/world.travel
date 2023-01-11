from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

from db.session import Base


class Countries(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    continent = Column(String(255), nullable=False)
    population = Column(Integer, nullable=False)
    cities = relationship("Cities", back_populates="country")
    user_travel_experiences = relationship("UserTravelExperiences", back_populates="country")


class Cities(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    population = Column(Integer, nullable=False)
    area = Column(Float, nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    country = relationship("Countries", back_populates="cities")
    attractions = relationship("Attractions", back_populates="city")
    hotels = relationship("Hotels", back_populates="city")
    restaurants = relationship("Restaurants", back_populates="city")
    weather = relationship("Weather", back_populates="city")
    user_travel_experiences = relationship("UserTravelExperiences", back_populates="city")


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    street = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    zipcode = Column(String(255), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    country = relationship("Countries", back_populates="addresses")
    hotels = relationship("Hotels", back_populates="address")
    restaurants = relationship("Restaurants", back_populates="address")


class Hotels(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
    rating = Column(Float, nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    address = relationship("Address", back_populates="hotels")
    city = relationship("Cities", back_populates="hotels")
    bookings = relationship("Booking", back_populates="hotel")
    content = relationship(
        "Content",
        back_populates="hotel",
        primaryjoin="and_(Hotels.id == Content.content_id, Content.content_type==Hotels.__tablename__)"
    )
    reviews = relationship(
        "Reviews",
        back_populates="hotel",
        primaryjoin="and_(Hotels.id == Reviews.review_id, Reviews.review_type==Hotels.__tablename__)"
    )


class Restaurants(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
    rating = Column(Float, nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    address = relationship("Address", back_populates="restaurants")
    city = relationship("Cities", back_populates="restaurants")
    bookings = relationship("Booking", back_populates="restaurant")
    tags = relationship("Tag", secondary="restaurant_tags")

    content = relationship(
        "Content",
        back_populates="restaurant",
        primaryjoin="and_(Restaurants.id == Content.content_id, Content.content_type==Restaurants.__tablename__)"
    )
    reviews = relationship(
        "Reviews",
        back_populates="restaurant",
        primaryjoin="and_(Restaurants.id == Reviews.review_id, Reviews.review_type==Restaurants.__tablename__)"
    )


class Weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    date = Column(Date, nullable=False)
    temperature = Column(Float, nullable=False)
    condition = Column(String(255), nullable=False)
    city = relationship("Cities", back_populates="weather")
