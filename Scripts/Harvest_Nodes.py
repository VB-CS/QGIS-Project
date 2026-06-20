from qgis.core import QgsProject, QgsField
from PyQt5.QtCore import QVariant
from collections import defaultdict

# 1. Access the layer
layer = QgsProject.instance().mapLayersByName('Clustered_Retail_Centers')[0]

# 2. Define business logic
anchor_tags = {'supermarket', 'pharmacy', 'convenience', 'department_store', 'mall'}
synergy_tags = {'hair_salon', 'beauty', 'restaurant', 'cafe', 'gym', 'bakery'}

# 3. Aggregate data
cluster_data = defaultdict(lambda: {'anchors': 0, 'synergy': 0, 'total': 0})

for f in layer.getFeatures():
    c_id = f['CLUSTER_ID']
    if c_id:
        shop = f['shop']
        cluster_data[c_id]['total'] += 1
        if shop in anchor_tags:
            cluster_data[c_id]['anchors'] += 1
        elif shop in synergy_tags:
            cluster_data[c_id]['synergy'] += 1

# 4. Add/Update Field 'FEASIBILITY_SCORE'
layer.startEditing()
if 'FEASIBILITY_SCORE' not in [f.name() for f in layer.fields()]:
    layer.dataProvider().addAttributes([QgsField('FEASIBILITY_SCORE', QVariant.Int)])
    layer.updateFields()

score_idx = layer.fields().indexOf('FEASIBILITY_SCORE')

for f in layer.getFeatures():
    c_id = f['CLUSTER_ID']
    if c_id and c_id in cluster_data:
        # Scoring Logic: 5 pts per anchor, 2 pts per synergy, 0.5 per total store
        stats = cluster_data[c_id]
        score = (stats['anchors'] * 5) + (stats['synergy'] * 2) + (stats['total'] * 0.5)
        f[score_idx] = int(score)
        layer.updateFeature(f)

layer.commitChanges()
print("SUCCESS: Feasibility scores calculated. Check your Attribute Table for 'FEASIBILITY_SCORE'.")