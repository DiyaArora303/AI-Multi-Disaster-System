import ee
import time

ee.Initialize(project='winter-internship-480719')

# Select MODIS LST
dataset = ee.ImageCollection("MODIS/006/MOD11A1") \
            .filterDate('2025-01-01', '2025-12-31') \
            .select('LST_Day_1km')

image = dataset.median()

# Region of interest (India subset)
region = ee.Geometry.Rectangle([72.5, 18.5, 77.5, 22.0])

# Export to Google Drive
task = ee.batch.Export.image.toDrive(
    image=image,
    description='heatwave_export',
    folder='EarthEngine',  # This folder will appear in your Google Drive
    fileNamePrefix='heatwave_2025',
    region=region.getInfo()['coordinates'],
    scale=1000,
    crs='EPSG:4326',
    maxPixels=1e13
)

task.start()
print("Export started. Please check Google Drive in a few minutes.")

# Optional: monitor status
while task.active():
    print("Exporting...")
    time.sleep(10)

print("Export completed! Check Google Drive folder 'EarthEngine'.")
