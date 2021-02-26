import logging
from typing import List

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from controller import controller 
from entity import schemas, models
from entity.database import SessionLocal


logger = logging.getLogger(__name__)
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/client",  response_model=List[schemas.Client],  status_code=200)
async def get(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return controller.get_clients(db, skip=skip, limit=limit)

@router.post("/client", response_model=schemas.Client, status_code=201)
async def register(
    client: schemas.ClientCreate,
    db: Session = Depends(get_db)
):
    try:
        return controller.create_clients(db=db, client=client)
    except KeyError as e:
        logger.error(str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/car",  response_model=List[schemas.Car],  status_code=200)
async def get(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return controller.get_cars(db, skip=skip, limit=limit)

@router.get("/client/{client_id}/",  response_model=schemas.Client,  status_code=200)
async def get(client_id: int, db: Session = Depends(get_db)):
    return controller.get_car_by_client(db,  client_id=client_id)

@router.post("/client/delete/{client_id}/", status_code=200)
async def get(
    client_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    return controller.delete_client(db,  client_id=client_id)


@router.post("/client/{client_id}/car/", response_model=schemas.Car)
async def create_car_for_client(
    client_id: int,
    car: schemas.CarCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        return controller.create_client_car(db=db, car=car, client_id=client_id)
    except KeyError as e:
        logger.error(str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/token/")
async def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    client = controller.authenticate_client(db=db, username=form_data.username, token=form_data.password)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )
    return {'access_token' : form_data.username + 'token'}