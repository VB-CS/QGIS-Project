## 1. Context & Problem Statement

- **Background:** The spatial pipeline processes 1,087 raw OpenStreetMap (OSM) retail nodes retrieved via the Overpass API to locate commercial clusters before running drive-time matrix queries through OpenRouteService.
- **Problem:** Standard distance partitioning or fixed-radius grouping fails to capture the irregular, non-spherical geographic footprints of real-world retail corridors, causing arbitrary cluster splits or incorporating non-commercial noise.
- **Scope:** Spatial cluster accuracy, API request efficiency, and downstream "Feasibility Score" calculation reliability.
- **Constraints:** The clustering algorithm must handle arbitrary spatial shapes and automatically identify sparse noise nodes without requiring a hardcoded cluster count.

---

## 2. Options Considered

### Option A: K-Means Spatial Clustering

- **Description:** Partition spatial coordinates into K centroids using Euclidean distance vectors.
- **Pros:** Computationally efficient with predictable performance characteristics.
- **Cons:** Requires defining the exact number of clusters (K) upfront; forces rigid spherical geometries that misalign with linear commercial strips along transit corridors.
- **Performance Trade-offs:** Fast processing time at the expense of high boundary distortion.

### Option B: DBSCAN Density-Based Clustering (Chosen)

- **Description:** Group coordinates based on local point density using explicit search radius (ε) and minimum sample threshold parameters.
- **Pros:** Discovers arbitrary cluster shapes and automatically isolates low-density, standalone retail nodes as noise.
- **Cons:** Highly sensitive to parameter tuning (ε and `min_samples`); performance can degrade across variable-density suburban zones.
- **Performance Trade-offs:** Requires careful hyper-parameter calibration in exchange for realistic commercial hub definitions.

---

## 3. Decision & Technical Rationale

**Chosen Option:** Option B (DBSCAN Clustering).

- Commercial retail hubs naturally form along irregular road networks rather than uniform circular zones. DBSCAN captures linear and non-standard geographic clusters while filtering out isolated stores, ensuring that drive-time matrix calculations and anchor-store synergy scores operate on true commercial centers.

---

## 4. Consequences & Trade-offs

### ✅ Positive System Impacts

- High-precision commercial hub identification and reduced API costs by excluding non-clustered noise nodes from matrix calculations.

### ⚠️ Potential Failure Points

- Static ε distance thresholds might under-cluster low-density suburban hubs or over-cluster dense urban cores.

### 🔧 Operational & Maintenance Costs

- Requires spatial parameter recalibration when scaling the pipeline to different metropolitan density profiles.
