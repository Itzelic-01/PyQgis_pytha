# 밀도 조건 반영 클러스터링

import os
import processing
from qgis.core import QgsProject, QgsVectorLayer
from qgis.analysis import QgsNativeAlgorithms

# Delete All Layers
# 현재 열려있는 레이어 전체 삭제 함수
def deleteAll() :
    project = QgsProject.instance()
    layer_ids = project.mapLayers().keys()

    for layer_id in layer_ids:
        project.removeMapLayer(layer_id)


def KmeansByDen(input):
    
    input_path = '/Users/sohyunkim/Desktop/works/부동산데이터작업/지역별건물shp/' + input + '/' + input + '_CLIP'
    output_path = '/Users/sohyunkim/Desktop/works/부동산데이터작업/지역별건물shp/' + input + '/' + input + '_Kmeans'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(output_path)
    
    i = 0
    # INCHEON_CLIP_0 ~ INCHEON_CLIP_1772 까지 적용
    for file in os.listdir(input_path):
        # shp 파일만 로드
        if file.endswith('.shp'):
            file_path = os.path.join(input_path, file)
            input_layer = QgsVectorLayer(file_path, 'input_layer', 'ogr')
            if not input_layer.isValid():
                print("Layer is not Available")
            else:
                num_features = input_layer.featureCount()
            
                # 밀도 계산 (클러스터 개수 k를 결정하는 기준)
                # extent() 함수로 포인트를 포함하는 사각형 도형을 생성, 
                # extent의 너비와 높이를 곱해 area 영역의 넓이를 구함
                extent = input_layer.extent()
                area = extent.width() * extent.height()
                
                # area가 0인 경우 (피처 수가 0개 or 1개인 경우)
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

                # output 경로 설정
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
                # output_layer = iface.addVectorLayer(output_path_, "", "ogr")
                i += 1

                print("처리 완료" + output_path_)

input = "INCHEON"
KmeansByDen(input)