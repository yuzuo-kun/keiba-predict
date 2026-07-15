from fastapi import APIRouter
from models.request import PredictRequest

router = APIRouter()

@router.post("/predict")
def predict(request: PredictRequest):
    return {
        "status": "success",
        "received_url": request.url
    }