from fastapi import APIRouter
from backend.models.landslide_model_loader import predict_landslide
import numpy as np

router = APIRouter(prefix="/landslide", tags=["Landslide"])

@router.post("/predict")
def landslide_predict(data: dict):
    features = np.array(data["features"])
    result = predict_landslide(features)
    return {"prediction": result}
