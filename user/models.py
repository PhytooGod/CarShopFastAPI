from sqlalchemy import Column, String, Integer, DateTime
from core.db import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    date = Column(DateTime)