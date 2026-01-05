import ee
import os
import geemap
import rasterio
from rasterio.merge import merge

# Initialize Earth Engine
ee.Initialize(project='winter-internship-480719')
os.makedirs("data_pipeline/raw", exist_ok=True)

# Define India bounding box
india = ee.Geometry.Rectangle([68, 6, 98, 38])

# Load flood dataset (50-year return period)
flood_img = ee.ImageCollection("JRC/CEMS_GLOFAS/FloodHazard/v2_1") \
              .select("RP50_depth") \
              .first()  # static hazard map

# Clip to India
flood_india = flood_img.clip(india)

# Split India into smaller tiles
def get_tiles(geometry, rows=2, cols=2):
    bounds = geometry.bounds().coordinates().get(0)
    coords = ee.List(bounds)
    x_min = ee.Number(ee.List(coords.get(0)).get(0))
    y_min = ee.Number(ee.List(coords.get(0)).get(1))
    x_max = ee.Number(ee.List(coords.get(2)).get(0))
    y_max = ee.Number(ee.List(coords.get(2)).get(1))
    
    x_step = x_max.subtract(x_min).divide(cols)
    y_step = y_max.subtract(y_min).divide(rows)
    
    tiles = []
    for i in range(rows):
        for j in range(cols):
            xmin = x_min.add(x_step.multiply(j))
            ymin = y_min.add(y_step.multiply(i))
            xmax = xmin.add(x_step)
            ymax = ymin.add(y_step)
            tiles.append(ee.Geometry.Rectangle([xmin, ymin, xmax, ymax]))
    return tiles

tiles = get_tiles(india, rows=2, cols=2)  # 4 tiles

# Export each tile
tile_paths = []
for idx, tile in enumerate(tiles):
    out_path = f"data_pipeline/raw/flood_50yr_india_tile{idx+1}.tif"
    tile_paths.append(out_path)
    print(f"Exporting tile {idx+1} to {out_path} ...")
    geemap.ee_export_image(
        flood_india,
        filename=out_path,
        scale=1000,  # adjust resolution
        region=tile,
        file_per_band=False
    )

print("All tiles exported. Merging into one file...")

# Merge tiles using rasterio
src_files_to_mosaic = [rasterio.open(p) for p in tile_paths]
mosaic, out_trans = merge(src_files_to_mosaic)

# Save the merged output
out_meta = src_files_to_mosaic[0].meta.copy()
out_meta.update({
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": out_trans,
    "compress": "lzw"
})

merged_path = "data_pipeline/raw/flood_50yr_india_merged.tif"
with rasterio.open(merged_path, "w", **out_meta) as dest:
    dest.write(mosaic)

# Close all tile files
for src in src_files_to_mosaic:
    src.close()

print(f"Merged flood data saved at: {merged_path}")
