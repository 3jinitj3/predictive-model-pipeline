from app.schemas.users import UserCreate, UserResponse
from app.db.session import AsyncSession
from app.db.models.users import Users
from sqlalchemy import select
from fastapi import HTTPException
from app.core.security import password_hash, verify_password
from app.schemas.auth import TokenData
from app.schemas.users import UserObject
from app.services.auth_service import auth_service
from app.db.session import database
from typing import Annotated

class UserServices:

    async def register(self, user:UserCreate, db:AsyncSession) -> UserResponse:
        result = await db.execute(
            select(Users).where(Users.username == user.username)
        )
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=400, detail='User already exists.')
        HASHED_PASSWORD = password_hash.hash(user.password)
        new_user = Users(
            first_name=user.first_name,
            last_name=user.last_name,
            birthdate=user.birthdate,
            username=user.username,
            passwd_hash=HASHED_PASSWORD,
            email=user.email
        )
        user.password = None
        db.add(new_user)
        await db.flush()
        return UserResponse(
            user_id=new_user.user_id,
            username=new_user.username,
            email=new_user.email
        )


    # Look at turning this into a dependency
    async def get_current_user(self, token:str, db:AsyncSession) -> UserObject:
        token_data = auth_service.decode_token(token=token)
        result = await db.execute(
            select(Users).where(Users.user_id == token_data.user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail='User does not exist')
        return UserObject(
            user_id=user.user_id,
            username=user.username,
            role_id=user.role_id,
            first_name=user.first_name,
            last_name=user.last_name
        )





user_service = UserServices()