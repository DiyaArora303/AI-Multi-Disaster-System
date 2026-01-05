from fastapi import APIRouter
from backend.models.cyclone_model_loader import predict_cyclone
import numpy as np

router = APIRouter(prefix="/cyclone", tags=["Cyclone"])

@router.post("/predict")
def cyclone_predict(data: dict):
    features = np.array(data["features"])
    result = predict_cyclone(features)
    return {"prediction": result}

