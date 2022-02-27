from pydantic import BaseModel  
from datetime import date

class Car(BaseModel):
    id : int 
    brand : str 
    title : str 
    date : date
    owner : int 
    
    class Config:
        orm_mode = True
    
class Owner(BaseModel):
    id : int
    name : str
    surname : str
    email : str
    date : date

    class Config:
        orm_mode = True