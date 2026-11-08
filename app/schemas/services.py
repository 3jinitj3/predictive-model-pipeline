# serviceCreate, serviceRead, serviceUpdate
from pydantic import BaseModel
from enum import Enum


class ServiceData(BaseModel):
    service_id: int
    service: str
    description: str
    price: float

