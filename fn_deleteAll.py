# Delete All Layers
# 현재 열려있는 레이어 전체 삭제 함수
def deleteAll() :
    project = QgsProject.instance()
    layer_ids = project.mapLayers().keys()

    for layer_id in layer_ids:
        project.removeMapLayer(layer_id)

deleteAll()