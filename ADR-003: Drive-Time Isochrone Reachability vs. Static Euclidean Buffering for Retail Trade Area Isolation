### 1. Context & Problem Statement

- **Background:** Evaluating commercial trade areas for retail site selection requires isolating competitive store density and consumer reachability around target market tracts.
- **Problem:** Standard radial distance buffers (e.g., a static 5-mile circular buffer) evaluate proximity "as the crow flies." This ignores physical barriers, traffic infrastructure, and actual travel time, leading to inaccurate market evaluation.
- **Scope:** Spatial bounding, Overpass API query efficiency, and point-in-polygon node clipping within the PyQGIS ETL pipeline.
- **Constraints:** Must isolate realistic consumer travel boundaries without introducing excessive REST API overhead or breaking downstream bounding box extraction.

---

## 2. Options Considered

### Option A: Static Euclidean Radius Buffering (Circular Buffers)

- **Description:** Draw a uniform radial circle (e.g., 5-mile radius) around target census tracts using standard geographic buffering (`native:buffer`).
- **Pros:** Computationally trivial with zero external network API dependencies; executes instantly in local memory.
- **Cons:** Geographically inaccurate. Includes stores across impassable rivers, rail yards, or highway disconnects that consumers cannot physically access in a typical shopping trip.
- **Performance Trade-offs:** Minimal CPU usage, but inflates downstream API payloads and processing overhead by fetching irrelevant, out-of-bounds store nodes.

### Option B: Network-Based Drive-Time Isochrones (Chosen)

- **Description:** Model travel-time envelopes (e.g., 20-minute drive-time) using OpenRouteService network routing data, paired with a two-tier spatial bounding box extraction and point-in-polygon clipping pipeline.
- **Pros:** Reflects actual consumer behavior, road networks, and physical barriers; eliminates false-positive competitor nodes outside true drive-time corridors.
- **Cons:** Generates complex, non-spherical polygon geometries that require explicit bounding box transformations (`EPSG:4326`) before API execution.
- **Performance Trade-offs:** Introduces network routing API latency during boundary retrieval in exchange for significantly cleaner downstream vector inputs and zero spatial noise.

---

## 3. Decision & Technical Rationale

**Chosen Option:** Option B (Network-Based Drive-Time Isochrones).

- Retail gravity and pedestrian foot traffic correlate with travel duration rather than straight-line geometric distance. Utilizing Isochrones isolates true commercial corridors without spatial bleed. To manage complex geometry with external REST endpoints, the PyQGIS pipeline extracts a tight WGS84 bounding box (`extract_wgs84_bbox`) to scope the initial Overpass API payload, then executes an in-memory spatial clip (`native:extractbylocation`) strictly inside the Isochrone boundary.

---

## 4. Consequences & Trade-offs

### ✅ Positive System Impacts

- Eliminates spatial noise and out-of-bounds competitor nodes prior to downstream DBSCAN clustering.
- Delivers realistic, defensible market feasibility scores based on real-world reachability rather than straight-line distance.

### ⚠️ Potential Failure Points

- External routing API downtime or rate-limiting could halt initial Isochrone polygon generation.

### 🔧 Operational & Maintenance Costs

- Requires maintaining a defensive two-tier spatial harvesting pattern (API bounding box fetch + local QGIS vector clip) to handle complex polygon boundaries safely.
