import numpy as np
import osmnx as ox, networkx as nx, geopandas as gpd, matplotlib.pyplot as plt
import seaborn as sns
import folium
import folium.plugins
import pandas as pd
from folium import plugins
from folium.plugins import MarkerCluster, HeatMap
import branca.colormap as cm
import json
import urllib.request
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import numbers
import math
from geopy.geocoders import Nominatim
from folium.utilities import normalize
from haversine import haversine
from shapely.geometry import Point, Polygon, LineString
from descartes import PolygonPatch
import requests
import matplotlib
import matplotlib.cm as cm
import matplotlib.colors as colors
import re
import pickle
import gzip
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

def getLatLng(request): #카카오 API를 이용하여 주소를 위도 경도를 반환합니다.
    
    if request.method == 'POST':
        '''plt.plot([1, 2, 3, 4])
        plt.ylabel('y-label')
        plt.show()
        '''
        
        departure = request.POST['departure']
        destination = request.POST['destination']
        url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query=' + departure
        url2 = 'https://dapi.kakao.com/v2/local/search/keyword.json?query=' + destination
        headers = {"Authorization": "KakaoAK 84ba6228f2f7a5f35ca89b1c459849ec"}
        result = json.loads(str(requests.get(url,headers=headers).text))
        result2 = json.loads(str(requests.get(url2,headers=headers).text))
        x = float(result['documents'][0]['x']) # 경도 - x축 기준
        y = float(result['documents'][0]['y']) # 위도 - y축 기준
        x2 = float(result2['documents'][0]['x']) # 경도 - x축 기준
        y2 = float(result2['documents'][0]['y']) # 위도 - y축 기준
        poc = (y,x)
        poc2 = (y2,x2)

        m = folium.Map(
        location = [37.5502, 126.982],
        zoom_start = 11.5)

        with gzip.open('prac/templates/prac/서울따릉이프로젝트그래프(압축버전).pickle','rb') as f: # 저장된 피클을 불러오는 파일입니다.
            Seoul_Map = pickle.load(f) 
           
        with gzip.open('prac/templates/prac/서울따릉이노드(압축버전).pickle','rb') as f:
            Seoul_Node = pickle.load(f)
            
        with gzip.open('prac/templates/prac/서울따릉이엣지(압축버전).pickle','rb') as f:
            Seoul_Edge = pickle.load(f)
        
        orig_node = ox.get_nearest_node(Seoul_Map, (y, x)) #시작점
        dest_node = ox.get_nearest_node(Seoul_Map, (y2, x2)) #도착지
        path= nx.shortest_path(Seoul_Map, orig_node, dest_node, weight = 'energy') #저희가 만든 최소 에너지 경로로 길을 찾습니다.
        
        '''
        lines = []
        #edges = []
        for i in path:

            try:
                if i == Seoul_Edge.loc[i,'geometry']:
                    a = str(a)
                    x = a.find('(')
                    y = a.find(')')
                    a = a[x+1:y]
                    a = a.split(',')

                    for j in a:
                        s = i.strip()
                        s = s.split(' ')
                        lines.append((float(s[1]), float(s[0])))

            except:
                pass

        for i in path:
            
            try:
                lines.append((Seoul_Node.loc[i,'y'],Seoul_Node.loc[i,'x']))

            except:
                pass
        
        lines = list(set(lines))
        print(lines)

        folium.Circle(
        location = lines,
        radius = 300
        ).add_to(m)
        
        folium.PolyLine(
            locations = lines,
            tooltip = 'PolyLine'
        ).add_to(m)
        
        m.save('prac/templates/prac/map.html')
        return render(request, 'prac/map.html')
        '''
        route_graph_map = ox.plot_route_folium(Seoul_Map, path, route_color='red', route_map=m, popup_attribute='length')
        path_length = int(sum(ox.utils_graph.get_route_edge_attributes(Seoul_Map, path, 'length')))
        print(path_length)
        #route_graph_map = (ox.plot_graph_route(Seoul_Map, path, 'c', route_linewidth=6, node_size=0))
        route_graph_map.save('prac/templates/prac/map.html')

        return render(request, 'prac/map.html')
        
        '''
        folium.Marker(
            location=[y,x],
            popup='출발지',
            icon=folium.Icon(color='blue',icon='star')
        ).add_to(m)

        folium.Marker(
            location=[y2,x2],
            popup='도착지',
            icon=folium.Icon(color='blue',icon='star')
        ).add_to(m)

        #root가 프로젝트 경로인듯
        m.save('prac/templates/prac/map.html')
        return render(request, 'prac/map.html')
        '''
        

def home(request):

    return render(request, 'prac/index.html')

def about(request):

    if request.method == "POST":
        
        departure = request.POST['departure']
        url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query=' + departure
        headers = {"Authorization": "KakaoAK 84ba6228f2f7a5f35ca89b1c459849ec"}
        result = json.loads(str(requests.get(url,headers=headers).text))
        x = float(result['documents'][0]['x']) # 경도 - x축 기준
        y = float(result['documents'][0]['y']) # 위도 - y축 기준
        poc = (y,x)
        
        api_key = '474753514f70687738345772516568' # 제 앱 키입니다. 실시간 자전거 정류장 위치 (공공데이터 API)
        def makeurl():
            return  'http://openapi.seoul.go.kr:8088/' + api_key + '/json/bikeList/1/1000/' # 제 개인적인 키입니다. 오남용 금지.
                
        def makeurl2():
            #return  'http://openapi.seoul.go.kr:8088/' + api_key + '/json/bikeList/1/1000/' # 제 개인적인 키입니다. 오남용 금지.
            return 'http://openapi.seoul.go.kr:8088/' + api_key + '/json/bikeList/1001/2000' #+ start +'/'+ end +'/' # 제 개인적인 키입니다.

        dic = {}
        url = makeurl() #'http://openapi.seoul.go.kr:8088/' + api_key + '/json/bikeList/1/1000/'
        url2 = makeurl2() #'http://openapi.seoul.go.kr:8088/' + api_key + '/json/bikeList/1001/2000/'

        req = urllib.request.urlopen(url).read().decode('utf-8')
        req2 = urllib.request.urlopen(url2).read().decode('utf-8')

        StaNum = [] # 역 이름과 번호 같이 있음
        StaNum_Only = [] # 정류장 번호만 담을 리스트입니다.
        StaNum_Name = [] # 정류장 이름만 담을 리스트 입니다.
        Cnt = [] # 현재 남아있는 자전거
        StaNum_wido = []
        StaNum_gyungdo = []
        StaNum_Tot = []
        StaNum_Rate = []
        jsonObject = json.loads(req)
        jsonObject2 = json.loads(req2)

        #1에서 1000까지
        for i in range(len(jsonObject['rentBikeStatus']['row'])):
            StaNum.append(jsonObject['rentBikeStatus']['row'][i]['stationName'])
            Cnt.append(int(jsonObject['rentBikeStatus']['row'][i]['parkingBikeTotCnt']))
            StaNum_wido.append(np.float64(jsonObject['rentBikeStatus']['row'][i]['stationLatitude']))
            StaNum_gyungdo.append(np.float64(jsonObject['rentBikeStatus']['row'][i]['stationLongitude']))
            StaNum_Tot.append(int(jsonObject['rentBikeStatus']['row'][i]['rackTotCnt']))
            
        for i in range(len(StaNum)):
            for j in range(len(StaNum[i])):
                if(StaNum[i][j]=='.'):
                    StaNum_Only.append(int(StaNum[i][0:j]))
                    StaNum_Name.append(StaNum[i][j+1:]) # 정류장 이름
                    break;


        #1001에서 끝까지
        for i in range(len(jsonObject2['rentBikeStatus']['row'])):
            StaNum_Only.append(int(jsonObject2['rentBikeStatus']['row'][i]['stationName'][0:4]))
            StaNum_Name.append(jsonObject2['rentBikeStatus']['row'][i]['stationName'][5:])
            '''
            이 구간은 전부 천의 자리 숫자라, 슬라이싱으로 앞의 4개의 인덱스만 잘라냈습니다. 
            위의 방법으로 하면 오류가 발생하는 구간이 존재하여 앞의 방식과 다르게 풀었습니다.
            '''
            Cnt.append(int(jsonObject2['rentBikeStatus']['row'][i]['parkingBikeTotCnt']))
            StaNum_wido.append(np.float64(jsonObject2['rentBikeStatus']['row'][i]['stationLatitude']))
            StaNum_gyungdo.append(np.float64(jsonObject2['rentBikeStatus']['row'][i]['stationLongitude']))
            StaNum_Tot.append(int(jsonObject2['rentBikeStatus']['row'][i]['rackTotCnt']))

        for i in range(len(jsonObject['rentBikeStatus']['row']) + len(jsonObject2['rentBikeStatus']['row'])):
            StaNum_Rate.append((Cnt[i]/StaNum_Tot[i]) * 100)
        
        BikeMap = {'정류장번호' : StaNum_Only, '정류장이름': StaNum_Name, '거치대갯수' : StaNum_Tot, 
                                '현재자전거갯수' : Cnt, '위도' : StaNum_wido, '경도' : StaNum_gyungdo, '충원율(단위 : %)' : StaNum_Rate}
        #dic = list_to_dictionary(StaNum_Only, Cnt) ## 딕셔너리로 만드는 함수 이용
        
        print(len(BikeMap['정류장번호']))

        m2 = folium.Map(
            location = [y, x],
            zoom_start = 14.5
            )
        
        for i in range(len(BikeMap['정류장번호'])):
            dist = haversine(poc, (BikeMap['위도'][i], BikeMap['경도'][i]), unit='km')
            if dist < 0.75:

                folium.Marker([BikeMap['위도'][i], BikeMap['경도'][i]], popup=BikeMap['정류장이름'][i], icon=folium.Icon(color='blue',icon='info-sign')).add_to(m2)
            
        m2.save('prac/templates/prac/about.html')
        return render(request, 'prac/about.html')

def homepage(request):
    
    return render(request, 'prac/homepage.html')