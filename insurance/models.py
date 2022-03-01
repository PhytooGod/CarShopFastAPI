from core.db import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, backref

class Insurance(Base):
    __tablename__ = "insurance"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    description = Column(String)
    date = Column(DateTime)
    expiredate = Column(DateTime)
    insurancelist = relationship('InsuranceList', backref='Insurance', passive_deletes=True)