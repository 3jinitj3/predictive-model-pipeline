from app.schemas.users import UserCreate, UserResponse
from app.db.session import AsyncSession
from app.db.models.users import Users
from sqlalchemy import select
from fastapi import HTTPException
from app.core.security import password_hash, verify_password

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



user_service = UserServices()