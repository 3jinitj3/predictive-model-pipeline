from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import database
from app.services.sales_service import delivery_service

router = APIRouter()

router.post('/services/{service_id}')
async def get_service(service_id: int, db=Annotated[AsyncSession, Depends(database.get_db)]):
    service = await delivery_service.get_service(service_id=service_id, db=db)
    return service