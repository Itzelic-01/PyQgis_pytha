# 밀도 조건 반영 클러스터링

import os
import processing
from qgis.core import QgsProject
from qgis.analysis import QgsNativeAlgorithms

def KmeansByDen(input):

    input_path = "/Users/sohyunkim/Desktop/works/부동산데이터작업/지역별건물shp/"+ input + "/" + input + "_CLIP"
    output_path = "/Users/sohyunkim/Desktop/works/부동산데이터작업/지역별건물shp/"+ input + "/" + input + "_Kmeans"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    i = 0
    for file in os.listdir(input_path):
        layer = iface.addVectorLayer(input_path, "", "ogr")
        
        num_features = layer.featureCount()
    
        # 밀도 계산 (클러스터 개수 k를 결정하는 기준)
        extent = layer.extent()
        area = extent.width() * extent.height()
        
        # 0으로 나뉘면 안됨
        if area == 0 :
            density = 0
            print("CLIP_", i, " - No Density : {}".format(density),"---", num_features, " features")
        else :
            density = num_features / area
            print("CLIP_", i, " - Density: {}".format(density)," ", num_features, " features")
            
        # density 기반 클러스터 개수 설정
        if density == 0 or density >= 0.01 :
            k = 1
        elif density >= 0.005 :
            k = 2
        else :
            k = 3
        
        ## k-means clustering 수행
        result = processing.run("native:kmeansclustering", {
            'INPUT' : layer,
            'FIELD_NAME' : 'cluster_id',
            'CLUSTERS' : k,
            'OUTPUT' : output_path
        })
        # 현재 레이어 전체 삭제
        project = QgsProject.instance()
        layer_ids = project.mapLayers().keys()

        for layer_id in layer_ids:
            project.removeMapLayer(layer_id)

        i+=1
        # Kmeans 적용된 output파일 경로출력
        output_path_ = output_path + '/Cluster_' + str(i) + '.shp'

input = "INCHEON"
KmeansByDen(input)