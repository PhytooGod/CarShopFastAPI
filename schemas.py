from pydantic import BaseModel  
from datetime import date

class UserLogin(BaseModel):
    username : str
    password : str

class User(BaseModel):
    username : str
    password : str
    email : str

class Car(BaseModel):
    brand : str 
    title : str 
    dateofcreation : date
    price : int
    owner : int 
    manager : int
    
    class Config:
        orm_mode = True
    
class Manager(BaseModel):
    name : str
    surname : str
    fee : float
    sellchance : float

    class Config:
        orm_mode = True

class Insurance(BaseModel):
    description : str
    expiredate : date

    class Config:
        orm_mode = True

class InsuranceList(BaseModel):
    car : int
    insurance : int

    class Config:
        orm_mode = True

class Owner(BaseModel):
    name : str
    surname : str
    email : str

    class Config:
        orm_mode = True
    
class Token(BaseModel):
    access_token : str