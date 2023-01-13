from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


from db.session import Base


class Donations(Base):
    __tablename__ = 'donations'
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    dream_id = Column(Integer, ForeignKey('dreams.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="donations")
    dream = relationship("Dream", back_populates="donations")
