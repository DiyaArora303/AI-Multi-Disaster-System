import ee
import geemap

ee.Initialize(project='winter-internship-480719')

# Define India bounding box
region = ee.Geometry.Rectangle([68.0, 6.0, 97.5, 36.0])

# Use a year with guaranteed data (e.g., 2020)
dataset = ee.ImageCollection("MODIS/006/MOD11A1") \
            .filterDate('2020-01-01', '2020-12-31')

# Print available bands
first_image = dataset.first()
print("Bands in the first image:", first_image.bandNames().getInfo())

# Select valid band
image = dataset.select('LST_Day_1km').median()

# Export to Google Drive
task = ee.batch.Export.image.toDrive(
    image=image,
    description='heatwave_export',
    folder='EarthEngine',
    fileNamePrefix='heatwave_India_2020',
    region=region,
    scale=1000,
    maxPixels=1e10
)
task.start()
print("✅ Export task started. Check your Google Drive 'EarthEngine' folder.")
