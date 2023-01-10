from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date

from db.session import Base


class Countries(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    continent = Column(String(255), nullable=False)
    population = Column(Integer, nullable=False)


class Cities(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    population = Column(Integer, nullable=False)
    area = Column(Float, nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)


class Attractions(Base):
    __tablename__ = 'attractions'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    street = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    zipcode = Column(String(255), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)


class Hotels(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
    rating = Column(Float, nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)


class Restaurants(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
    rating = Column(Float, nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)


class Weather(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    date = Column(Date, nullable=False)
    temperature = Column(Float, nullable=False)
    condition = Column(String(255), nullable=False)
