import os
import json
from shapely.geometry import shape, Point
import geopandas as gpd

def point_in_shapefile(lat, lon, shapefile_path):
    if not os.path.exists(shapefile_path):
        return {}
    gdf = gpd.read_file(shapefile_path)
    pt = Point(lon, lat)
    res = gdf[gdf.geometry.contains(pt)]
    if res.empty:
        return {}
    return res.iloc[0].to_dict()
