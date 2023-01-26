import os
import pandas as pd
import geopandas as gpd

# Merge Point SHP Files + add xy field
# input에 지역 이름 문자열이 들어오면 해당 경로에 있는 클러스터 중심점 파일들에 대해 파일 병합을 수행
# 병합된 파일에 x, y 좌표 추가해서 shp 파일로 추출

def MergeP(input):
    input_path = '/Users/sohyunkim/Desktop/works/부동산데이터작업/지역별건물shp/' + input + '/' + input + '_ClusterP'
    output_path = "/Users/sohyunkim/Desktop/works/부동산데이터작업/지역별건물shp/"+ input + "/" + input + "_ResultP"
    # 해당 경로에 해당 폴더 없으면 생성
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # input_path 경로에 있는 shp파일 리스트
    shp_files = [f for f in os.listdir(input_path) if f.endswith('.shp')]
    # 결과 저장할 geopandas dataframe
    merged_gdf = gpd.GeoDataFrame()
    
    for shp in shp_files:
        gdf = gpd.read_file(os.path.join(input_path, shp))

        # 데이터프레임에 xy좌표 추가
        gdf['x'] = gdf.geometry.x
        gdf['y'] = gdf.geometry.y

        merged_gdf = pd.concat([merged_gdf, gdf])

    merged_gdf.to_file(os.path.join(output_path, 'ClusterPoint.shp'))

input_MergeP = "INCHEON"
MergeP(input_MergeP)