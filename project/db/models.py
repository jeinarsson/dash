from sqlalchemy import Column, \
    Integer, String, Text, DateTime, Boolean, PickleType
from sqlalchemy.orm import relationship

from project.db import Base

class EventsCache(Base):
    __tablename__ = 'eventscache'
    id = Column(Integer, primary_key=True)

    timestamp = Column(DateTime)
    data = Column(PickleType)

