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
import matplotlib.pyplot as plt
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import numbers
import math
from geopy.geocoders import Nominatim
from folium.utilities import normalize
import googlemaps
from haversine import haversine
from shapely.geometry import Point, Polygon, LineString
from descartes import PolygonPatch
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors
import re
import pickle
import gzip
from copy import deepcopy
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render


def getLatLng(request): #카카오 API를 이용하여 주소를 위도 경도를 반환합니다.
    
    if request.method == 'POST':
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
        '''    
        with gzip.open('prac/templates/prac/서울따릉이노드(압축버전).pickle','rb') as f:
            Seoul_Node = pickle.load(f)
            
        with gzip.open('prac/templates/prac/서울따릉이엣지(압축버전).pickle','rb') as f:
            Seoul_Edge = pickle.load(f)
        '''

        orig_node = ox.get_nearest_node(Seoul_Map, (y, x)) #시작점
        dest_node = ox.get_nearest_node(Seoul_Map, (y2, x2)) #도착지
        path= nx.shortest_path(Seoul_Map, orig_node, dest_node, weight = 'energy') #저희가 만든 최소 에너지 경로로 길을 찾습니다.
        print(path)
        route_graph_map = ox.plot_graph_route(Seoul_Map, path, 'c', route_linewidth=6, node_size=0)
        #route_graph_map.save('prac/templates/prac/map.html')

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