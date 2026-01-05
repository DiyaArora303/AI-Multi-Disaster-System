from backend.models.flood_model_loader import predict_flood

def run_flood_prediction(raster_patch):
    return predict_flood(raster_patch)
