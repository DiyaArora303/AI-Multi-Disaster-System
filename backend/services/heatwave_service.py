from backend.models.heatwave_model_loader import predict_heatwave_from_tmax

def run_heatwave_prediction(date_str, tmax):
    return predict_heatwave_from_tmax(date_str, tmax)
