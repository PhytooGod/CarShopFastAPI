from core.db import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship 

class Car(Base):
    __tablename__ = "car"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    brand = Column(String)
    title = Column(String)
    date = Column(DateTime)
    owner = Column(Integer, ForeignKey("owner.id"))
    owner_id = relationship("Owner")