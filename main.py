from fastapi import FastAPI, status, HTTPException
from schemas import Car, Owner
from core.db import SessionLocal
from typing import List
import owner.models as models
import CarShop.models as carmodels

app = FastAPI()
db = SessionLocal()

@app.get('/cars', response_model=List[Car], status_code=200)
def get_all_cars():
    cars = db.query(carmodels.Car).all()
    return cars

@app.get('/car/{pk}', response_model=Car, status_code=status.HTTP_200_OK)
def get_car(pk:int):
    car=db.query(carmodels.Car).filter(carmodels.Car.id==pk).first()
    return car

@app.post('/cars', response_model=Car, status_code=status.HTTP_201_CREATED)
def add_car(car:Car):
    if db.query(models.Owner).filter(models.Owner.id == car.owner).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such owner")

    new_car = carmodels.Car(
        brand = car.brand,
        title = car.title,
        date = car.date,
        owner = car.owner
    )

    db.add(new_car)
    db.commit()

    return new_car


@app.put('/car/{pk}', response_model=Car, status_code=status.HTTP_200_OK)
def update_car(pk: int, car: Car):
    new_car = db.query(carmodels.Car).filter(carmodels.Car.id == pk).first()
    new_car.name = car.name
    new_car.surname = car.surname
    new_car.email = car.email
    new_car.date = car.date
    
    db.commit()

    return new_car

@app.delete('/car/{pk}')
def delete_car(pk: int):
    car_to_delete = db.query(carmodels.Car).filter(carmodels.Car.id == pk).first()
    
    if car_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such car")
    
    db.delete(car_to_delete)
    db.commit()

    return car_to_delete

@app.get('/owners',response_model=List[Owner], status_code=200)
def get_all_owners():
    owners=db.query(models.Owner).all()
    return owners


@app.get('/owner/{pk}', response_model=Owner, status_code=status.HTTP_200_OK)
def get_owner(pk:int):
    owner=db.query(models.Owner).filter(models.Owner.id==pk).first()
    return owner

@app.post('/owners', response_model=Owner, status_code=status.HTTP_201_CREATED)
def add_owner(owner:Owner):
    new_owner = models.Owner(
        name = owner.name,
        surname = owner.surname,
        email = owner.email,
        date = owner.date
    )

    db.add(new_owner)
    db.commit()

    return new_owner


@app.put('/owner/{pk}', response_model=Owner, status_code=status.HTTP_200_OK)
def update_owner(pk: int, owner: Owner):
    new_owner = db.query(models.Owner).filter(models.Owner.id == pk).first()
    new_owner.name = owner.name
    new_owner.surname = owner.surname
    new_owner.email = owner.email
    new_owner.date = owner.date
    
    db.commit()

    return new_owner

@app.delete('/owner/{pk}')
def delete_owner(pk: int):
    owner_to_delete = db.query(models.Owner).filter(models.Owner.id == pk).first()
    
    if owner_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such owner")
    
    db.delete(owner_to_delete)
    db.commit()

    return owner_to_delete