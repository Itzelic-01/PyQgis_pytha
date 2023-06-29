# 밀도 조건 반영 클러스터링

import os
import processing
from qgis.core import QgsProject, QgsVectorLayer
from qgis.analysis import QgsNativeAlgorithms

def KmeansByDen(input):
    
    input_path = '/파일경로' + input + '/' + input + '_CLIP'
    output_path = '/파일경로' + input + '/' + input + '_Kmeans'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(output_path)
    
    i = 0
    for file in os.listdir(input_path):
        # input_path_ = input_path + '/INCHEON_CLIP_' + str(i) + '.shp'
        # output_path_ = output_path + '/Cluster_' + str(i) + '.shp'
        if file.endswith('.shp'):
            file_path = os.path.join(input_path, file)
            input_layer = QgsVectorLayer(file_path, 'input_layer', 'ogr')
            if not input_layer.isValid():
                print("Layer is not Available")
            else:
                num_features = input_layer.featureCount()
            
                # 밀도 계산 (클러스터 개수 k를 결정하는 기준)
                extent = input_layer.extent()
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
                print(k)

                file_name = 'Kmeans_' + str(i) + '.shp'
                output_path_ = os.path.join(output_path, file_name)
                print(output_path_)
                ## k-means clustering 수행
                result = processing.run("native:kmeansclustering", {
                    'INPUT' : input_layer,
                    'FIELD_NAME' : 'cluster_id',
                    'CLUSTERS' : k,
                    'OUTPUT' : output_path_
                })
                output_layer = iface.addVectorLayer(output_path_, "", "ogr")
                i += 1

                print("처리 완료 : " + output_path_)

input = "INCHEON"
KmeansByDen(input)
