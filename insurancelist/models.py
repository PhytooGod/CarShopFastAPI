from core.db import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship 

class InsuranceList(Base):
    __tablename__ = "insurancelist"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    car = Column(Integer, ForeignKey("car.id"))
    car_id = relationship("Car")
    insurance = Column(Integer, ForeignKey("insurance.id"))
    insurance_id = relationship("Insurance")