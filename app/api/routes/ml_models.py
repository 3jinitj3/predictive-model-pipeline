from fastapi import APIRouter
from app.schemas.ml_models import MLModels



router = APIRouter()

@router.post('/models/{model_name}')
async def get_model(model_name: MLModels):
    pass