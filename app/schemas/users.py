# userCreate with password, userRead without password

import uuid
from fastapi_users import schemas
from pydantic import Field, field_validator, EmailStr, BaseModel
from datetime import datetime, date



class UserCreate(schemas.BaseUserCreate):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    birthdate: date
    username: str =Field(max_length=50)
    password: str = Field(min_length=12, max_length=128, description='Password must be atleat 12 characters.')
    email: EmailStr

    @field_validator('birthdate')
    @classmethod
    def validate_birth_date(cls, value:str):
        try:
            desired_format = datetime.strftime(value, '%m-%d-%Y')
            return desired_format
        except ValueError:
            raise ValueError('Birthdate must be in MM-DD-YYYY format')


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr


class UserObject(BaseModel):
    user_id: int
    username: str
    role_id: int
    first_name: str
    last_name: str
    org_id: int
