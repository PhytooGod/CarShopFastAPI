from core.db import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, backref

class Manager(Base):
    __tablename__ = "manager"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    surname = Column(String)
    fee = Column(Float)
    sellchance = Column(Float)
    car = relationship('Car', backref='Manager', passive_deletes=True)