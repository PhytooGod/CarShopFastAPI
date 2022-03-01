from sqlalchemy import Column, String, Integer, DateTime
from core.db import Base
from sqlalchemy.orm import relationship, backref

class Owner(Base):
    __tablename__ = "owner"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True)
    date = Column(DateTime)
    car = relationship('Car', backref='Owner', passive_deletes=True)