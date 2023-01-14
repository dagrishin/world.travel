import uuid

from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role_id = city_id = Column(UUID, ForeignKey('roles.id'), nullable=False)
    is_active = Column(Boolean(), default=True)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean(), default=False)

    role = relationship("Roles", back_populates="users")
    reviews = relationship("Reviews", back_populates="user")
    user_travel_experiences = relationship("UserTravelExperiences", back_populates="user")
    bookings = relationship("Booking", back_populates="user")
    tracks = relationship("Track", back_populates="user")
    places = relationship("Place", back_populates="user")
    donations = relationship("Donations", back_populates="user")
    dreams = relationship("Dreams", back_populates="user")

    content = relationship(
        "Content",
        back_populates="user",
        primaryjoin="and_(User.id == foreign(Content.content_id), Content.content_type=='users')"
    )


class RoleTypeEnum(Enum):
    ADMIN = 'admin'
    USER = 'user'
    GUEST = 'guest'


class Roles(Base):
    __tablename__ = 'roles'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(RoleTypeEnum(name='role_type'), default=RoleTypeEnum.USER)
    users = relationship("Users", back_populates="role")


class UserRoles(Base):
    __tablename__ = 'user_roles'
    user_id = Column(UUID, ForeignKey('users.id'), primary_key=True)
    role_id = Column(UUID, ForeignKey('roles.id'), primary_key=True)
