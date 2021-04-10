from django.shortcuts import render
import numpy as np
import osmnx as ox, networkx as nx, geopandas as gpd, matplotlib.pyplot as plt
import seaborn as sns
import folium
import folium.plugins
import pandas as pd
from folium import plugins
from folium.plugins import MarkerCluster
import branca.colormap as cm
import json
import urllib.request
import matplotlib.pyplot as plt
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import numbers
import math
from geopy.geocoders import Nominatim
from folium import plugins
from folium.utilities import normalize
from folium.plugins import HeatMap
import googlemaps
from haversine import haversine
from shapely.geometry import Point, Polygon, LineString
from descartes import PolygonPatch
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors
from django.shortcuts import render
from django.http import HttpResponse

def getLatLng(request): #카카오 API를 이용하여 주소를 위도 경도를 반환합니다.

    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query=서울대학교'
    headers = {"Authorization": "KakaoAK 84ba6228f2f7a5f35ca89b1c459849ec"}
    result = json.loads(str(requests.get(url,headers=headers).text))
    x = float(result['documents'][0]['x']) # 경도 - x축 기준
    y = float(result['documents'][0]['y']) # 위도 - y축 기준
    poc = (x,y)
    return HttpResponse(poc)
