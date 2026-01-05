from backend.models.cyclone_model_loader import predict_cyclone

def run_cyclone_prediction(lat, lon, wind_speed, pressure):
    return predict_cyclone([wind_speed, pressure, lat, lon])
