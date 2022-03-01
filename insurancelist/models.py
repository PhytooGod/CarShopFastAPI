from core.db import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, backref


class InsuranceList(Base):
    __tablename__ = "insurancelist"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    car = Column(Integer, ForeignKey("car.id", ondelete='CASCADE'))
    insurance = Column(Integer, ForeignKey("insurance.id", ondelete='CASCADE'))