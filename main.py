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
from authentication.jwt_handler import signJWT, decodeJWT
from authentication.jwt_bearer import jwtBearer
import logging
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

logging.basicConfig(filename="CarShopLogs.log", format='%(asctime)s %(message)s', filemode='a')
app = FastAPI()
db = SessionLocal()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@app.post('/user/signup', status_code=status.HTTP_201_CREATED)
def user_signup(user: User):
    logger.debug('user_signup function called.')
    new_user = usermodels.User(
        username = user.username,
        password = user.password,
        email = user.email,
        date = datetime.today()
    )   

    db.add(new_user)
    db.commit()
    logger.info(f'new user added to database status code: {status.HTTP_201_CREATED}')
    return signJWT(new_user.username)

def check_user(userlogin: UserLogin):
    logging.debug('check_user function called')
    if db.query(usermodels.User).filter(usermodels.User.username==userlogin.username and usermodels.User.password == userlogin.password).first() is None:
        logging.info("user's login and password doesn't match with any record in database")
        return False
    logging.info("user's login and password are correct")    
    return True 

@app.post('/user/login', status_code=status.HTTP_200_OK)
def user_login(userlogin: UserLogin):
    logging.debug(f'user_login function called')
    if check_user(userlogin):
        logging.debug(f'signJWT function called with username: {userlogin.username} status code: {status.HTTP_200_OK}')
        return signJWT(userlogin.username)
    else:
        logging.warning(f'Invalid username or password status code: {status.HTTP_400_BAD_REQUEST}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not valid username or password")


@app.get('/cars', response_model=List[Car], status_code=status.HTTP_200_OK)
def get_all_cars():
    logging.debug(f"get all cars function called")
    cars = db.query(carmodels.Car).all()
    logging.info(f"Cars recieved from database status code: {status.HTTP_200_OK}")
    return cars

@app.get('/car/{pk}', response_model=Car, status_code=status.HTTP_200_OK)
def get_car(pk:int):
    logging.debug(f"get car function called")
    car=db.query(carmodels.Car).filter(carmodels.Car.id==pk).first()
    if car is None:
        logging.error(f"No car with such ID status code: {status.HTTP_404_NOT_FOUND}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such car")
    logging.info(f"Car with id {pk} recieved from database status code: {status.HTTP_200_OK}")
    return car

@app.post('/cars', dependencies=[Depends(jwtBearer())], response_model=Car, status_code=status.HTTP_201_CREATED)
def add_car(car:Car, token: str = Depends(jwtBearer())):
    username = decodeJWT(token)['username']
    logging.debug(f"{username} trying to add new owner")
    if db.query(ownermodels.Owner).filter(ownermodels.Owner.id == car.owner).first() is None:
        logging.error(f"{username} is writing owner id that doesn't exist status code: {status.HTTP_404_NOT_FOUND}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such owner")

    if db.query(managermodels.Manager).filter(managermodels.Manager.id == car.manager).first() is None:
        logging.error(f"{username} is writing manager id that doesn't exist status code: {status.HTTP_404_NOT_FOUND}")
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
    logging.info(f"user={username}|Message=added new car into database|status code={status.HTTP_201_CREATED}")

    return new_car


@app.put('/car/{pk}', dependencies=[Depends(jwtBearer())], response_model=Car, status_code=status.HTTP_200_OK)
def update_car(pk: int, car: Car, token: str = Depends(jwtBearer())):
    username = decodeJWT(token)['username']
    logging.debug(f"{username} trying to update car with id {pk}")
    if db.query(ownermodels.Owner).filter(ownermodels.Owner.id == car.owner).first() is None:
        logging.error(f"{username} is writing owner id that doesn't exist status code: {status.HTTP_404_NOT_FOUND}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such owner")
    if db.query(managermodels.Manager).filter(managermodels.Manager.id == car.manager).first() is None:
        logging.error(f"{username} is writing manager id that doesn't exist status code: {status.HTTP_404_NOT_FOUND}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such manager")

    new_car = db.query(carmodels.Car).filter(carmodels.Car.id == pk).first()
    new_car.brand = car.brand
    new_car.title = car.title
    new_car.dateofcreation = car.dateofcreation
    new_car.price = car.price
    new_car.owner = car.owner
    new_car.manager = car.manager

    db.commit()
    logging.info(f"{username} updated car with id: {pk} successfully status code: {status.HTTP_200_OK}")
    return new_car

@app.delete('/car/{pk}', dependencies=[Depends(jwtBearer())], status_code=status.HTTP_200_OK)
def delete_car(pk: int, token: str = Depends(jwtBearer())):
    username = decodeJWT(token)['username']
    logging.debug(f"{username} trying to delete car with id {pk}")
    car_to_delete = db.query(carmodels.Car).filter(carmodels.Car.id == pk).first()
    
    if car_to_delete is None:
        logging.error(f"{username} is trying to delete the car that doesn't exist status code: {status.HTTP_404_NOT_FOUND}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such car")
    
    db.delete(car_to_delete)
    db.commit()
    logging.info(f"{username} deleted car with id: {pk} status code: {status.HTTP_200_OK}")
    return car_to_delete

@app.get('/owners',response_model=List[Owner], status_code=status.HTTP_200_OK)
def get_all_owners():
    logging.debug("get all owners function is called")
    owners=db.query(ownermodels.Owner).all()
    logging.info(f"all owners recieved from database status code: {status.HTTP_200_OK}")
    return owners


@app.get('/owner/{pk}', response_model=Owner, status_code=status.HTTP_200_OK)
def get_owner(pk:int):
    logging.debug('get owner function called')
    owner=db.query(ownermodels.Owner).filter(ownermodels.Owner.id==pk).first()
    logging.info(f"owner with id {pk} recieved from database status code: {status.HTTP_200_OK}")
    return owner

@app.post('/owners', dependencies=[Depends(jwtBearer())], response_model=Owner, status_code=status.HTTP_201_CREATED)
def add_owner(owner:Owner, token: str = Depends(jwtBearer())):
    username = decodeJWT(token)['username']
    logging.debug(f"{username} trying to add new owner")
    new_owner = ownermodels.Owner(
        name = owner.name,
        surname = owner.surname,
        email = owner.email,
        date = datetime.today()
    )

    db.add(new_owner)
    db.commit()
    logging.info(f"{username} added new owner to database with status code: {status.HTTP_201_CREATED}")

    return new_owner


@app.put('/owner/{pk}', dependencies=[Depends(jwtBearer())], response_model=Owner, status_code=status.HTTP_200_OK)
def update_owner(pk: int, owner: Owner, token: str = Depends(jwtBearer())):
    username = decodeJWT(token)['username']
    logging.debug(f"{username} trying to update owner with id: {pk}")
    new_owner = db.query(ownermodels.Owner).filter(ownermodels.Owner.id == pk).first()
    new_owner.name = owner.name
    new_owner.surname = owner.surname
    new_owner.email = owner.email
    new_owner.date = datetime.today()
    
    db.commit()
    logging.info(f"{username} updated owner with id: {pk} status code: {status.HTTP_200_OK}")
    return new_owner

@app.delete('/owner/{pk}', dependencies=[Depends(jwtBearer())])
def delete_owner(pk: int, token: str = Depends(jwtBearer())):
    username = decodeJWT(token)['username']
    logging.debug(f"{username} trying to delete owner with id {pk}")
    owner_to_delete = db.query(ownermodels.Owner).filter(ownermodels.Owner.id == pk).first()
    
    if owner_to_delete is None:
        logging.error(f"{username} is trying to delete owner that doesn't exist status code: {status.HTTP_404_NOT_FOUND}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such owner")
    
    db.delete(owner_to_delete)
    db.commit()
    logging.info(f"{username} deleted owner with id {pk} status code: {status.HTTP_200_OK}")
    return owner_to_delete


@app.get('/managers', response_model=List[Manager], status_code=200)
def get_all_managers():
    logging.debug('get all managers function called')
    managers = db.query(managermodels.Manager).all()
    logging.info(f"Managers recieved from database status code: {status.HTTP_200_OK}")
    return managers

@app.get('/manager/{pk}', response_model=Manager, status_code=status.HTTP_200_OK)
def get_manager(pk:int):
    logging.debug("get manager function called")
    manager=db.query(managermodels.Manager).filter(managermodels.Manager.id==pk).first()
    logging.info(f"Car with id {pk} recieved from database status code: {status.HTTP_200_OK}")
    return manager

@app.post('/managers', dependencies=[Depends(jwtBearer())], response_model=Manager, status_code=status.HTTP_201_CREATED)
def add_manager(manager:Manager, token: str = Depends(jwtBearer())):
    username = decodeJWT(token)['username']
    logging.debug(f"{username} trying to add new manager")
    new_manager = managermodels.Manager(
        name = manager.name,
        surname = manager.surname,
        fee = manager.fee,
        sellchance = manager.sellchance
    )

    db.add(new_manager)
    db.commit()
    logging.info(f"{username} added new manager to database with status code: {status.HTTP_201_CREATED}")
    return new_manager


@app.put('/manager/{pk}', dependencies=[Depends(jwtBearer())], response_model=Manager, status_code=status.HTTP_200_OK)
def update_manager(pk: int, manager: Manager, token: str = Depends(jwtBearer())):
    username = decodeJWT(token)['username']
    logging.debug(f"{username} trying to update manager with id {pk}")
    new_manager = db.query(managermodels.Manager).filter(managermodels.Manager.id == pk).first()
    new_manager.name = manager.name
    new_manager.surname = manager.surname
    new_manager.fee = manager.fee
    new_manager.sellchance = manager.sellchance

    db.commit()
    logging.info(f"{username} updated manager with id: {pk} status code: {status.HTTP_200_OK}")
    return new_manager

@app.delete('/manager/{pk}', dependencies=[Depends(jwtBearer())])
def delete_manager(pk: int, token: str = Depends(jwtBearer())):
    username = decodeJWT(token)['username']
    logging.debug(f"{username} trying to delete manager with id {pk}")
    manager_to_delete = db.query(managermodels.Manager).filter(managermodels.Manager.id == pk).first()
    
    if manager_to_delete is None:
        logging.error(f"{username} is trying to delete manager that doesn't exist status code: {status.HTTP_404_NOT_FOUND}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such manager")
    
    db.delete(manager_to_delete)
    db.commit()
    logging.info(f"{username} deleted manager with id {pk} status code: {status.HTTP_200_OK}")
    return manager_to_delete


@app.get('/insurance', response_model=List[Insurance], status_code=200)
def get_all_insurances():
    logging.debug("get all insurances function called")
    insurance = db.query(insurancemodels.Insurance).all()
    logging.info(f"Insurances recieved from database status code: {status.HTTP_200_OK}")
    return insurance

@app.get('/insurance/{pk}', response_model=Insurance, status_code=status.HTTP_200_OK)
def get_insurance(pk:int):
    logging.debug("get insurance function called")
    insurance=db.query(insurancemodels.Insurance).filter(insurancemodels.Insurance.id==pk).first()
    logging.info(f"Insurance with id {pk} recieved from database status code: {status.HTTP_200_OK}")
    return insurance

@app.post('/insurance', dependencies=[Depends(jwtBearer())], response_model=Insurance, status_code=status.HTTP_201_CREATED)
def add_insurance(insurance: Insurance, token: str = Depends(jwtBearer())):
    username = decodeJWT(token)['username']
    logging.debug(f"{username} trying to add new insurace")
    new_insurance = insurancemodels.Insurance(
        description = insurance.description,
        date = datetime.today(),
        expiredate = insurance.expiredate
    )

    db.add(new_insurance)
    db.commit()
    logging.info(f"{username} added new insurance to database with status code: {status.HTTP_201_CREATED}")
    return new_insurance


@app.put('/insurance/{pk}', dependencies=[Depends(jwtBearer())], response_model=Insurance, status_code=status.HTTP_200_OK)
def update_insurance(pk: int, insurance: Insurance, token: str = Depends(jwtBearer())):
    username = decodeJWT(token)['username']
    logging.debug(f"{username} trying to update insurance with id {pk}")
    new_insurance = db.query(insurancemodels.Insurance).filter(insurancemodels.Insurance.id == pk).first()
    new_insurance.description = insurance.description
    new_insurance.date = datetime.today()
    new_insurance.expiredate = insurance.expiredate
    db.commit()
    logging.info(f"{username} updated insurance with id: {pk} status code: {status.HTTP_200_OK}")
    return new_insurance

@app.delete('/insurance/{pk}', dependencies=[Depends(jwtBearer())])
def delete_insurance(pk: int, token: str = Depends(jwtBearer())):
    username = decodeJWT(token)['username']
    logging.debug(f"{username} trying to delete insurance with id {pk}")
    insurance_to_delete = db.query(insurancemodels.Insurance).filter(insurancemodels.Insurance.id == pk).first()
    
    if insurance_to_delete is None:
        logging.error(f"{username} is trying to delete insurance that doesn't exist status code: {status.HTTP_404_NOT_FOUND}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such insurance")
    
    db.delete(insurance_to_delete)
    db.commit()
    logging.info(f"{username} deleted insurance with id {pk} status code: {status.HTTP_200_OK}")
    return insurance_to_delete



@app.get('/insuranceslist', response_model=List[InsuranceList], status_code=200)
def get_all_insuranceslist():
    logging.debug("get all insurance list function called")
    insuranceslist = db.query(insurancelistmodels.InsuranceList).all()
    logging.info(f"Insurance Lists recieved from database status code: {status.HTTP_200_OK}")
    return insuranceslist

@app.get('/insurancelist/car/{pk}', response_model=List[InsuranceList], status_code=status.HTTP_200_OK)
def get_car_insurancelist(pk:int):
    logging.debug("get car insurance lists function called")
    carinsurancelist=db.query(insurancelistmodels.InsuranceList).filter(insurancelistmodels.InsuranceList.car==pk).all()
    logging.info(f"Insurance Lists of car with id {pk} recieved from database status code: {status.HTTP_200_OK}")
    return carinsurancelist

@app.get('/insurancelist/insurance/{pk}', response_model=List[InsuranceList], status_code=status.HTTP_200_OK)
def get_insurance_insurancelist(pk:int):
    logging.debug("get insurances insurance lists function called")
    insuranceinsurancelist=db.query(insurancelistmodels.InsuranceList).filter(insurancelistmodels.InsuranceList.insurance==pk).all()
    logging.info(f"Insurance Lists of insurance with id {pk} recieved from database status code: {status.HTTP_200_OK}")
    return insuranceinsurancelist

@app.post('/insurancelist', dependencies=[Depends(jwtBearer())], response_model=InsuranceList, status_code=status.HTTP_201_CREATED)
def add_insurancelist(insurancelist: InsuranceList, token: str = Depends(jwtBearer())):
    username = decodeJWT(token)['username']
    logging.debug(f"{username} trying to add new insurancelist")
    if db.query(carmodels.Car).filter(carmodels.Car.id == insurancelist.car).first() is None:
        logging.error(f"{username} writing car id that doesn't exist status code: {status.HTTP_404_NOT_FOUND}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such Car")

    if db.query(insurancemodels.Insurance).filter(insurancemodels.Insurance.id == insurancelist.insurance).first() is None:
        logging.error(f"{username} writing insurance id that doesn't exist status code: {status.HTTP_404_NOT_FOUND}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such insurance")

    new_insurancelist = insurancelistmodels.InsuranceList(
        car = insurancelist.car,
        insurance = insurancelist.insurance
    )

    db.add(new_insurancelist)
    db.commit()
    logging.info(f"{username} added new insurancelist to database with status code: {status.HTTP_201_CREATED}")
    return new_insurancelist


@app.put('/insurancelist/{pk}', dependencies=[Depends(jwtBearer())], response_model=InsuranceList, status_code=status.HTTP_200_OK)
def update_insurancelist(pk: int, insurancelist: InsuranceList, token: str = Depends(jwtBearer())):
    username = decodeJWT(token)['username']
    logging.debug(f"{username} trying to update insurancelist with id {pk}")
    if db.query(carmodels.Car).filter(carmodels.Car.id == insurancelist.car).first() is None:
        logging.error(f"{username} writing car id that doesn't exist status code: {status.HTTP_404_NOT_FOUND}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such Car")

    if db.query(insurancemodels.Insurance).filter(insurancemodels.Insurance.id == insurancelist.insurance).first() is None:
        logging.error(f"{username} writing insurance id that doesn't exist status code: {status.HTTP_404_NOT_FOUND}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such insurance")

    new_insurancelist = db.query(insurancelistmodels.InsuranceList).filter(insurancelistmodels.InsuranceList.id == pk).first()
    new_insurancelist.car = insurancelist.car
    new_insurancelist.insurance = insurancelist.insurance
    logging.info(f"{username} updated insurancelist with id: {pk} status code: {status.HTTP_200_OK}")
    db.commit()

    return new_insurancelist

@app.delete('/insurancelist/{pk}', dependencies=[Depends(jwtBearer())])
def delete_insurancelist(pk: int, token: str = Depends(jwtBearer())):
    username = decodeJWT(token)['username']
    logging.debug(f"{username} trying to delete insurancelist with id {pk}")
    insurancelist_to_delete = db.query(insurancelistmodels.InsuranceList).filter(insurancelistmodels.InsuranceList.id == pk).first()
    
    if insurancelist_to_delete is None:
        logging.error(f"{username} is trying to delete insurancelist that doesn't exist status code: {status.HTTP_404_NOT_FOUND}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such insurancelist")
    
    db.delete(insurancelist_to_delete)
    db.commit()
    logging.info(f"{username} deleted insurancelist with id {pk} status code: {status.HTTP_200_OK}")
    return insurancelist_to_delete