# File: backend/services/zones_service.py

import geopandas as gpd
import numpy as np # <--- CRITICAL FIX: Added numpy import

def get_critical_zones(disaster_type):
    """
    Returns GeoJSON of high-risk zones based on disaster predictions
    """
    # NOTE: You must have the GeoJSON/shapefile data available at this path.
    gdf = gpd.read_file(f"backend/shared/preprocess/gadm41_IND_1.shp")  # example admin division
    
    # For simplicity: mark all zones with some dummy 'risk_score'
    gdf['risk_score'] = np.random.rand(len(gdf)) # Fixed: np is now defined
    gdf['critical'] = gdf['risk_score'] > 0.7
    return gdf.to_json()