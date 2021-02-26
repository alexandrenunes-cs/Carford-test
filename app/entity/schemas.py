from enum import Enum
from typing import TYPE_CHECKING, List, Optional, Union

from pydantic import BaseModel

class CarColor(str, Enum):
    YELLOW = "yellow" 
    BLUE = "blue"  
    GRAY = "gray"  

class CarModel(str, Enum):
    HATCH = "hatch" 
    SEDAN = "sedan"  
    CONVERTIBLE = "convertible"  

class CarBase(BaseModel):    
    color: CarColor
    model: CarModel


class CarCreate(CarBase):
    pass

class Car(CarBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class ClientBase(BaseModel):
    username: str
    token: str

class ClientCreate(ClientBase):
    pass

class Client(ClientCreate):
    id: int
    is_active: bool
    sales_op: bool
    cars: List[Car] = []

    class Config:
        orm_mode = True
