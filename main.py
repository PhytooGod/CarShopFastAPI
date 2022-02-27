from fastapi import FastAPI, status, HTTPException
from schemas import Car, Owner
from core.db import SessionLocal
from typing import List
import owner.models as models
 
app = FastAPI()
db = SessionLocal()

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