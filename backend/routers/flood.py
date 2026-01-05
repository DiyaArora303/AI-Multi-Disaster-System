from fastapi import APIRouter
from backend.models.flood_model_loader import predict_flood
import numpy as np

router = APIRouter(prefix="/flood", tags=["Flood"])

@router.post("/predict")
def flood_predict(data: dict):
    flood_input = np.array(data["features"])
    result = predict_flood(flood_input)
    return {"prediction": result}
