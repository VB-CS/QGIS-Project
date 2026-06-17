from qgis.core import QgsProject, QgsRasterLayer

print("\n" + "="*60)
print("RUNNING AUTOMATED GEOSPATIAL INGESTION PIPELINE")
print("="*60)

# 1. Properly format the XYZ URI connection string for the core raster engine
osm_uri = "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png"

# 2. Use QgsRasterLayer with the explicit 'wms' provider for tile streams
osm_layer = QgsRasterLayer(osm_uri, "OpenStreetMap Base Layer", "wms")

# 3. Ingestion Integrity Verification Engine
if not osm_layer.isValid():
    print("PIPELINE ALERT: Spatial layer initialization failed validation checks.")
else:
    # Safely commit the verified raster layer into the active canvas project instance
    QgsProject.instance().addMapLayer(osm_layer)
    print("SUCCESS: Ingested 'OpenStreetMap Base Layer' into the active project registry.")
    print("PIPELINE STATUS: Ingestion complete. Canvas frame refreshed successfully.\n")