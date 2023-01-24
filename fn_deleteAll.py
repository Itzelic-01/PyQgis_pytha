# 현재 레이어 전체 삭제
def deleteAll() :
    project = QgsProject.instance()
    layer_ids = project.mapLayers().keys()

    for layer_id in layer_ids:
        project.removeMapLayer(layer_id)

deleteAll()