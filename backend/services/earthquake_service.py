from backend.models.earthquake_model_loader import predict_earthquake

def run_earthquake_prediction(lat, lon, magnitude):
    features = [magnitude, lat, lon]
    pred, prob = predict_earthquake(features)
    # Map model output to severity label if needed
    return {"prediction": pred, "probability": prob}
