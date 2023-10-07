from datetime import datetime
from enum import Enum

from pydantic import BaseModel

import easy_pysy as ez


class PetType(str, Enum):
    CAT = 'CAT'
    DOG = 'DOG'
    BIRD = 'BIRD'


class Pet(BaseModel):
    id: str
    name: str
    type: PetType
    owner_id: str


class Visit(BaseModel):
    id: str
    pet: Pet
    price: float
    at: datetime


class Owner(BaseModel):
    id: str
    name: str
    address: str


class VisitBooked(ez.Event):
    visit: Visit


class PetCreated(ez.Event):
    pet: Pet

