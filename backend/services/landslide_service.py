from backend.models.landslide_model_loader import predict_landslide

def run_landslide_prediction(lat, lon, slope, rainfall_24h, soil_moisture):
    features = [slope, rainfall_24h, soil_moisture, lat, lon]
    return predict_landslide(features)
