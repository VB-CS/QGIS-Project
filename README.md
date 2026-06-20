# Geospatial Retail White Space Analysis

# The Objective
To identify highly profitable, unsaturated real estate locations for new apparel retail placement within a 20-minute drive-time isochrone of Sugar Land/Richmond.

## Methodology
1. **Data Harvesting:** Extracted raw node data using OpenStreetMap (OSM).
2. **Isochrone Generation:** Created a 20-minute drive-time boundary to define the target consumer trade area.
3. **Clustering & Scoring:** Used Python to cluster retail nodes and assign a "Feasibility Score" based on the Gravity Model.

## The Findings
Applying the filter (`"CENTER_TYPE" = 'Non-Apparel Center'`) revealed that the primary market is entirely saturated. By pivoting to secondary markets, I successfully isolated multiple non-apparel centers (Feasibility Scores 6–14) that represent viable expansion points.

## Tech Stack
* **Language:** Python
* **Tools:** QGIS, OpenStreetMap(OSM), VSCode

