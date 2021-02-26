from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    token = Column(String)
    sales_op = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)

    cars = relationship("Car", cascade="all, delete")

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    color = Column(String)
    model = Column(String)
    owner_id = Column(Integer, ForeignKey("clients.id"))


