# Every file here must lead to an endpint service, users, services
# Think endpoint query, html pages 

# users used for sign up 'ME'
# Token endpoint, email and password for access token
# Responses to no such user and wrong password should be identical for security
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import database, Database
from app.schemas.users import UserCreate
from app.services.user_service import user_service

database1 = Database()
async_engine = database1.create_session_objects()
database1.meta_create_all(async_engine)

router = APIRouter(tags=['api.users'])

@router.post('/register', status_code=201)
async def register(user: UserCreate, session: Annotated[AsyncSession, Depends(database.get_db)]):
    try:
        user_response = await user_service.register(user=user, db=session)
        await session.commit()
        return {'message': 'User Created', 'username': user_response.username}
    except Exception:
        await session.rollback()
        raise 
