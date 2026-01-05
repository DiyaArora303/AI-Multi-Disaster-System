from fastapi import APIRouter
from backend.models.earthquake_model_loader import predict_earthquake

router = APIRouter(prefix="/earthquake", tags=["Earthquake"])

@router.post("/predict")
def earthquake_predict(data: dict):
    features = data["features"]
    result = predict_earthquake(features)
    return {"prediction": result}
