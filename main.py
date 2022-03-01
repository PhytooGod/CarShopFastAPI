from fastapi import FastAPI, status, HTTPException, Depends
from schemas import Car, Owner, Manager, Insurance, InsuranceList, User, UserLogin
from datetime import datetime
from core.db import SessionLocal
from typing import List, Optional
import owner.models as ownermodels
import CarShop.models as carmodels
import manager.models as managermodels
import insurance.models as insurancemodels
import insurancelist.models as insurancelistmodels
import user.models as usermodels
from authentication.jwt_handler import signJWT
from authentication.jwt_bearer import jwtBearer

app = FastAPI()
db = SessionLocal()

@app.post('/user/signup')
def user_signup(user: User):
    new_user = usermodels.User(
        username = user.username,
        password = user.password,
        email = user.email,
        date = datetime.today()
    )   

    db.add(new_user)
    db.commit()

    return signJWT(new_user.username)

def check_user(userlogin: UserLogin):
    if db.query(usermodels.User).filter(usermodels.User.username==userlogin.username and usermodels.User.password == userlogin.password).first() is None:
        return False
    return True 

@app.post('/user/login')
def user_login(userlogin: UserLogin):
    if check_user(userlogin):
        return signJWT(userlogin.username)
    else:
        return {
            "error":"Invalid login details"
        }

@app.get('/cars', response_model=List[Car], status_code=200)
def get_all_cars():
    cars = db.query(carmodels.Car).all()
    return cars

@app.get('/car/{pk}', response_model=Car, status_code=status.HTTP_200_OK)
def get_car(pk:int):
    car=db.query(carmodels.Car).filter(carmodels.Car.id==pk).first()
    if car is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such car")
    return car

@app.post('/cars', response_model=Car, status_code=status.HTTP_201_CREATED)
def add_car(car:Car):
    if db.query(ownermodels.Owner).filter(ownermodels.Owner.id == car.owner).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such owner")

    if db.query(managermodels.Manager).filter(managermodels.Manager.id == car.manager).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such manager")

    new_car = carmodels.Car(
        brand = car.brand,
        title = car.title,
        dateofcreation = car.dateofcreation,
        price = car.price,
        owner = car.owner,
        manager = car.manager
    )

    db.add(new_car)
    db.commit()

    return new_car


@app.put('/car/{pk}', response_model=Car, status_code=status.HTTP_200_OK)
def update_car(pk: int, car: Car):
    if db.query(ownermodels.Owner).filter(ownermodels.Owner.id == car.owner).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such owner")

    if db.query(managermodels.Manager).filter(managermodels.Manager.id == car.manager).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such manager")

    new_car = db.query(carmodels.Car).filter(carmodels.Car.id == pk).first()
    new_car.brand = car.brand
    new_car.title = car.title
    new_car.dateofcreation = car.dateofcreation
    new_car.price = car.price
    new_car.owner = car.owner
    new_car.manager = car.manager

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
    owners=db.query(ownermodels.Owner).all()
    return owners


@app.get('/owner/{pk}', response_model=Owner, status_code=status.HTTP_200_OK)
def get_owner(pk:int):
    owner=db.query(ownermodels.Owner).filter(ownermodels.Owner.id==pk).first()
    return owner

@app.post('/owners', dependencies=[Depends(jwtBearer())],response_model=Owner, status_code=status.HTTP_201_CREATED)
def add_owner(owner:Owner):
    new_owner = ownermodels.Owner(
        name = owner.name,
        surname = owner.surname,
        email = owner.email,
        date = datetime.today()
    )

    db.add(new_owner)
    db.commit()

    return new_owner


@app.put('/owner/{pk}', response_model=Owner, status_code=status.HTTP_200_OK)
def update_owner(pk: int, owner: Owner):
    new_owner = db.query(ownermodels.Owner).filter(ownermodels.Owner.id == pk).first()
    new_owner.name = owner.name
    new_owner.surname = owner.surname
    new_owner.email = owner.email
    new_owner.date = datetime.today()
    
    db.commit()

    return new_owner

@app.delete('/owner/{pk}')
def delete_owner(pk: int):
    owner_to_delete = db.query(ownermodels.Owner).filter(ownermodels.Owner.id == pk).first()
    
    if owner_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such owner")
    
    db.delete(owner_to_delete)
    db.commit()
    return owner_to_delete


@app.get('/managers', response_model=List[Manager], status_code=200)
def get_all_managers():
    managers = db.query(managermodels.Manager).all()
    return managers

@app.get('/manager/{pk}', response_model=Manager, status_code=status.HTTP_200_OK)
def get_manager(pk:int):
    manager=db.query(managermodels.Manager).filter(managermodels.Manager.id==pk).first()
    return manager

@app.post('/managers', response_model=Manager, status_code=status.HTTP_201_CREATED)
def add_manager(manager:Manager):
    new_manager = managermodels.Manager(
        name = manager.name,
        surname = manager.surname,
        fee = manager.fee,
        sellchance = manager.sellchance
    )

    db.add(new_manager)
    db.commit()

    return new_manager


@app.put('/manager/{pk}', response_model=Manager, status_code=status.HTTP_200_OK)
def update_manager(pk: int, manager: Manager):
    new_manager = db.query(managermodels.Manager).filter(managermodels.Manager.id == pk).first()
    new_manager.name = manager.name
    new_manager.surname = manager.surname
    new_manager.fee = manager.fee
    new_manager.sellchance = manager.sellchance

    db.commit()

    return new_manager

@app.delete('/manager/{pk}')
def delete_manager(pk: int):
    manager_to_delete = db.query(managermodels.Manager).filter(managermodels.Manager.id == pk).first()
    
    if manager_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such manager")
    
    db.delete(manager_to_delete)
    db.commit()

    return manager_to_delete


@app.get('/insurance', response_model=List[Insurance], status_code=200)
def get_all_insurances():
    insurance = db.query(insurancemodels.Insurance).all()
    return insurance

@app.get('/insurance/{pk}', response_model=Insurance, status_code=status.HTTP_200_OK)
def get_insurance(pk:int):
    insurance=db.query(insurancemodels.Insurance).filter(insurancemodels.Insurance.id==pk).first()
    return insurance

@app.post('/insurance', response_model=Insurance, status_code=status.HTTP_201_CREATED)
def add_insurance(insurance: Insurance):
    new_insurance = insurancemodels.Insurance(
        description = insurance.description,
        date = datetime.today(),
        expiredate = insurance.expiredate
    )

    db.add(new_insurance)
    db.commit()

    return new_insurance


@app.put('/insurance/{pk}', response_model=Insurance, status_code=status.HTTP_200_OK)
def update_insurance(pk: int, insurance: Insurance):
    new_insurance = db.query(insurancemodels.Insurance).filter(insurancemodels.Insurance.id == pk).first()
    new_insurance.description = insurance.description
    new_insurance.date = datetime.today()
    new_insurance.expiredate = insurance.expiredate
    db.commit()

    return new_insurance

@app.delete('/insurance/{pk}')
def delete_insurance(pk: int):
    insurance_to_delete = db.query(insurancemodels.Insurance).filter(insurancemodels.Insurance.id == pk).first()
    
    if insurance_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such insurance")
    
    db.delete(insurance_to_delete)
    db.commit()

    return insurance_to_delete



@app.get('/insuranceslist', response_model=List[InsuranceList], status_code=200)
def get_all_insuranceslist():
    insuranceslist = db.query(insurancelistmodels.InsuranceList).all()
    return insuranceslist

@app.get('/insurancelist/car/{pk}', response_model=List[InsuranceList], status_code=status.HTTP_200_OK)
def get_car_insurancelist(pk:int):
    carinsurancelist=db.query(insurancelistmodels.InsuranceList).filter(insurancelistmodels.InsuranceList.car==pk).all()
    return carinsurancelist

@app.get('/insurancelist/insurance/{pk}', response_model=List[InsuranceList], status_code=status.HTTP_200_OK)
def get_insurance_insurancelist(pk:int):
    insuranceinsurancelist=db.query(insurancelistmodels.InsuranceList).filter(insurancelistmodels.InsuranceList.insurance==pk).all()
    return insuranceinsurancelist

@app.post('/insurancelist', response_model=InsuranceList, status_code=status.HTTP_201_CREATED)
def add_insurancelist(insurancelist: InsuranceList):
    if db.query(carmodels.Car).filter(carmodels.Car.id == insurancelist.car).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such Car")

    if db.query(insurancemodels.Insurance).filter(insurancemodels.Insurance.id == insurancelist.insurance).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such insurance")

    new_insurancelist = insurancelistmodels.InsuranceList(
        car = insurancelist.car,
        insurance = insurancelist.insurance
    )

    db.add(new_insurancelist)
    db.commit()

    return new_insurancelist


@app.put('/insurancelist/{pk}', response_model=InsuranceList, status_code=status.HTTP_200_OK)
def update_insurancelist(pk: int, insurancelist: InsuranceList):
    if db.query(carmodels.Car).filter(carmodels.Car.id == insurancelist.car).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such Car")

    if db.query(insurancemodels.Insurance).filter(insurancemodels.Insurance.id == insurancelist.insurance).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such insurance")

    new_insurancelist = db.query(insurancelistmodels.InsuranceList).filter(insurancelistmodels.InsuranceList.id == pk).first()
    new_insurancelist.car = insurancelist.car
    new_insurancelist.insurance = insurancelist.insurance

    db.commit()

    return new_insurancelist

@app.delete('/insurancelist/{pk}')
def delete_insurancelist(pk: int):
    insurancelist_to_delete = db.query(insurancelistmodels.InsuranceList).filter(insurancelistmodels.InsuranceList.id == pk).first()
    
    if insurancelist_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such insurancelist")
    
    db.delete(insurancelist_to_delete)
    db.commit()

    return insurancelist_to_delete