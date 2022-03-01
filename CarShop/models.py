from core.db import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

class Car(Base):
    __tablename__ = "car"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    brand = Column(String)
    title = Column(String)
    dateofcreation = Column(DateTime)
    price = Column(Integer)
    owner = Column(Integer, ForeignKey("owner.id", ondelete='CASCADE'))
    manager = Column(Integer, ForeignKey("manager.id", ondelete='CASCADE'))
    InsuranceList = relationship('InsuranceList', backref='Car', passive_deletes=True)