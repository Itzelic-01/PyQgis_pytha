import os
from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsField, QgsProject
from qgis.PyQt.QtCore import QVariant

# Get Cluster Center Point
# 해당 지역(영문)을 입력하면 kmeans_clustering이 적용된 폴더의 경로를 찾아 
# 각 shp파일을 순회하며 같은 cluster_id에 속하는 클러스터들의 밀도의 중심점을 찾는 알고리즘

def GetClusterP(input):
    input_path = '/Users/sohyunkim/Desktop/works/부동산데이터작업/지역별건물shp/' + input + '/' + input + '_Kmeans'
    output_path = '/Users/sohyunkim/Desktop/works/부동산데이터작업/지역별건물shp/' + input + '/' + input + '_ClusterP'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    i = 0
    for file in os.listdir(input_path):
        # shp파일만 순회
        if file.endswith('.shp'):
            file_path = os.path.join(input_path, file)
            input_layer = QgsVectorLayer(file_path, 'input_layer', 'ogr')
            if not input_layer.isValid():
                print("Layer is not Available")
            else:

                # output용 새 벡터레이어 생성 (상가 관련 좌표계는 5174로 설정)
                output_layer = QgsVectorLayer('Point?crs=epsg:5174', 'output_layer', 'memory')

                # output레이어에 cluster_id 컬럼 추가
                output_layer.dataProvider().addAttributes([QgsField('cluster_id', QVariant.Int)])

                # x, y좌표 기재 dictionary
                cluster_dict = {}

                # input레이어의 각 피처에 대해 반복
                features = input_layer.getFeatures()
                for feature in features:
                    # get the cluster_id attribute value
                    cluster_id = feature['cluster_id']
                    
                    # xy좌표 가져오기
                    x, y = feature.geometry().asPoint()
                    
                    # cluster_id기 dictionary에 없으면 추가하고 xy좌표의 합계를 0으로 표기
                    if cluster_id not in cluster_dict:
                        cluster_dict[cluster_id] = {'x_sum': 0, 'y_sum': 0, 'count': 0}
                    
                    # 현재 cluster_id에 해당하는 x 및 y 좌표의 합계
                    cluster_dict[cluster_id]['x_sum'] += x
                    cluster_dict[cluster_id]['y_sum'] += y
                    cluster_dict[cluster_id]['count'] += 1

                # dictionary안의 cluster_id 순회
                for cluster_id, cluster_data in cluster_dict.items():
                    # 각 cluster_id에 대해 x, y 평균좌표 구하기(밀도의 중심점 계산)
                    avg_x = cluster_data['x_sum'] / cluster_data['count']
                    avg_y = cluster_data['y_sum'] / cluster_data['count']
                    
                    # output feature 생성
                    output_feature = QgsFeature()
                    
                    # 피처에 평균점 도형 생성
                    output_feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(avg_x, avg_y)))
                    
                    # 피처의 cluster_id 속성 설정
                    output_feature.setAttributes([cluster_id])
                    
                    # output features를 output layer에 추가
                    output_layer.dataProvider().addFeature(output_feature)

                # output layer를 shp파일로 추출 (ClusterP_번호.shp)
                file_name = 'ClusterP_' + str(i)
                output_path_ = os.path.join(output_path, file_name)
                QgsVectorFileWriter.writeAsVectorFormat(output_layer, output_path_,
                'utf-8', output_layer.crs(), 'ESRI Shapefile')

                i += 1
                
                print(output_path_)

input = "INCHEON"
GetClusterP(input)
