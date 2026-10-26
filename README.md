# Geospatial Retail White-Space Analysis

A Python/QGIS geospatial analysis designed to identify potential expansion locations for apparel retail within a 20-minute drive-time trade area around Sugar Land and Richmond, Texas. The workflow combines OpenStreetMap retail-location data, a drive-time isochrone, density-based spatial clustering, and a gravity-model feasibility score to support a market-entry decision.

## Business question

Where are there plausible retail expansion opportunities in and around the target trade area, and which candidate locations appear less saturated than the primary market?

## Methodology

### 1. Data harvesting — OpenStreetMap

Extract raw OSM retail nodes for the study area as the input to the location analysis. The project summary reports 1,087 raw OSM nodes before filtering and analysis.

### 2. Trade-area generation — OpenRouteService (ORS) isochrone

Generate a 20-minute driving isochrone using OpenRouteService (ORS). This network-based boundary represents the target travel-time area more realistically than a simple circular buffer around a center point.

### 3. Spatial clustering — DBSCAN

Use DBSCAN (Density-Based Spatial Clustering of Applications with Noise) to identify density-connected groups of retail nodes and to mark isolated observations as noise rather than forcing every point into a cluster.

DBSCAN was selected instead of K-means because the workflow does not need to predefine a number of clusters and because density-connected clusters can follow irregular spatial patterns more naturally than centroid-based groupings. K-means requires a chosen `k` and tends to favor compact, roughly spherical clusters.

**Parameter note:** DBSCAN is sensitive to its neighborhood distance (`eps`) and `min_samples`. A single `eps` can perform poorly if local point densities vary substantially. The distance metric and coordinate units must agree; do not treat longitude/latitude degrees as meters.

### 4. Feasibility scoring — gravity-model approach

Assign a `Feasibility Score` to candidate centers using the project's gravity-model approach. The score is used as a prioritization signal for comparing expansion candidates, not as a guarantee of commercial performance.

## Findings

The initial analysis indicated that the primary market was saturated under the applied center-type filter (`CENTER_TYPE = 'Non-Apparel Center'`). Pivoting to secondary markets surfaced multiple candidate non-apparel centers with feasibility scores in the **6–14** range, representing locations for further investigation.

The decision implication was to look beyond the initially saturated area rather than assume the primary market contained the best remaining white space. Scores should be interpreted alongside the underlying data, assumptions, and local market context.

## Tech stack

- **Language:** Python
- **GIS and visualization:** QGIS
- **Retail-location data:** OpenStreetMap (OSM)
- **Drive-time boundary:** OpenRouteService (ORS) isochrone
- **Spatial clustering:** DBSCAN
- **Development:** Visual Studio Code

## Repository contents

- `Scripts/` — analysis scripts (review the folder for the execution order and inputs).
- `Assets/` — project assets and supporting data.
- `*.qgz` — QGIS project file.
- `docs/` — architecture decision record for the spatial clustering choice.

## Reproducibility and limitations

- Confirm that ORS credentials, request limits, and the isochrone parameters are configured for your local environment before rerunning the workflow.
- OSM coverage and tagging quality vary; missing, duplicate, or misclassified locations can affect the results.
- Cluster outcomes depend on the input subset, coordinate handling, DBSCAN parameters, and selected distance metric.
- A gravity-model feasibility score is a screening tool. It should not be treated as a substitute for validating demand, competition, lease cost, accessibility, and local market conditions.
- Preserve the original CRS/coordinate transformation assumptions when reproducing distance calculations.

## Architecture decisions

See [`docs/README.md`](docs/README.md) for the documented DBSCAN clustering decision.
