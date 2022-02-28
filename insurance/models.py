from core.db import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship 

class Insurance(Base):
    __tablename__ = "insurance"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    description = Column(String)
    date = Column(DateTime)
    expiredate = Column(DateTime)