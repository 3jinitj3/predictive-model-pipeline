# Every file here must lead to an endpint service, users, services
# Think endpoint query, html pages 

# users used for sign up 'ME'
# Token endpoint, email and password for access token
# Responses to no such user and wrong password should be identical for security
from typing import Annotated
from fastapi import APIRouter, Depends 
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import database
from app.schemas.users import UserCreate, UserObject
from app.services.user_service import user_service
from app.services.auth_service import auth_service
from fastapi.security import OAuth2PasswordBearer



router = APIRouter(tags=['users'])


# Create user account
@router.post('/register', status_code=201)
async def register(user: UserCreate, session: Annotated[AsyncSession, Depends(database.get_db)]):
    try:
        user_response = await user_service.register(user=user, db=session)
        await session.commit()
        return {'message': 'User Created', 'username': user_response.username}
    except Exception:
        await session.rollback()
        raise 


# This would be the users home page
@router.get('/users/me', status_code=200)
async def get_me(
    token: Annotated[str, Depends(auth_service.oauth2_schema)],
    db: Annotated[AsyncSession, Depends(database.get_db)]) -> UserObject:
    return await user_service.get_current_user(token=token, db=db)


