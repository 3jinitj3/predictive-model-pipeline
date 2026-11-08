from fastapi import APIRouter, Depends
from app.schemas.services import ServiceData
from app.schemas.users import UserObject
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import database

router = APIRouter()


@router.post('/purchase_order')
async def purchase_order(
    service_data: ServiceData,
    user_object: UserObject,
    db:Annotated[AsyncSession, Depends(database.get_db)])
    
    result = 