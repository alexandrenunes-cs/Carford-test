import logging
import re
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from passlib.hash import pbkdf2_sha256

from entity import models
from entity import schemas


logger = logging.getLogger(__name__)

def create_clients(db: Session, client: schemas.ClientCreate):
    
    db_client = get_client_by_name(db, username=client.username)
    if db_client:
        raise Exception("Client already registered")
    fake_hashed_password = pbkdf2_sha256.hash(client.token)
    db_client = models.Client(username=client.username, token=fake_hashed_password)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_client_by_name(db: Session, username: str):
    return db.query(models.Client).filter(models.Client.username == username).first()

def get_client(db: Session, client_id: int):
    db_client =  db.query(models.Client).filter(models.Client.id == client_id).first()
    return db_client

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    db_client =  db.query(models.Client).offset(skip).limit(limit).all()
    return db_client

def delete_client(db: Session, client_id: int):
    db_client =  db.query(models.Client).filter(models.Client.id == client_id).first()
    db.delete(db_client)
    db.commit()
    return True

def get_cars(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Car).offset(skip).limit(limit).all()

def create_client_car(db: Session, car: schemas.CarCreate, client_id: int):
    db_client = get_client(db, client_id=client_id)
    if not db_client:
        raise Exception("Client is not registered")
    if client_has_limit_cars(db, client_id=client_id):
        raise Exception("Client has reached the limit of 3 cars")
    db_car = models.Car(**car.dict(), owner_id=client_id)
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

def client_has_limit_cars(db: Session, client_id: int):
    db_client =  db.query(models.Client).filter(models.Client.id == client_id).first()
    if len(db_client.cars) < 3:
        return False
    return True

def authenticate_client(db: Session, username: str, token: str):
    client = db.query(models.Client).filter(models.Client.username == username).first()
    if not client:
        return False 
    if not pbkdf2_sha256.verify(token, client.token):
        return False
    return client 

