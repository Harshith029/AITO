from fastapi import APIRouter
from ..models.schemas import PredictionInput
from app.services.trafficapp_predictor import predict_traffic

router = APIRouter()

@router.post("/")
def get_prediction(data: PredictionInput):
    prediction = predict_traffic(data)
    return {"predicted_traffic_level": prediction}
