from fastapi import APIRouter
from backend.models.heatwave_model_loader import predict_heatwave
import numpy as np

router = APIRouter(prefix="/heatwave", tags=["Heatwave"])

@router.post("/predict")
def heatwave_predict(data: dict):
    features = np.array(data["features"])
    result = predict_heatwave(features)
    return {"prediction": result}
