from typing import Annotated
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import database
from app.services.auth_service import auth_service



router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post(path='/login')
async def user_login(
    response: Response,
    credentials: Annotated[OAuth2PasswordRequestForm,  Depends()],
    db: Annotated[AsyncSession, Depends(database.get_db)]
):
    token_data = await auth_service.verify_login(credentials=credentials, db=db)
    access_token = auth_service.create_access_token(token_data=token_data)
    refresh_token = auth_service.create_refresh_token(token_data=token_data)
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=30
    )

    return {'access_token': access_token, 'token_type': 'bearer'}

# When you need to continue working with the object use session.refresh(new_user) or session.flush()
# create audit_log record for db
# login
# refresh
# logout
# verify token
# current user
# password reset