from fastapi import APIRouter
import rasterio
import numpy as np

router = APIRouter(prefix="/population", tags=["Population"])

@router.post("/at_risk")
def population_at_risk(data: dict):
    """
    data: {"lat": , "lon": , "radius": } 
    returns estimated population at risk from population.tif
    """
    lat, lon, radius = data["lat"], data["lon"], data.get("radius", 0.1)
    with rasterio.open("data_pipeline/raw/population.tif") as src:
        row, col = src.index(lon, lat)
        window = src.read(1, window=rasterio.windows.Window(col-radius, row-radius, radius*2, radius*2))
        pop = np.sum(window)
    return {"population_at_risk": int(pop)}
