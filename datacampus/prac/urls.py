from django.urls import path
from . import views

urlpatterns = [
    path('getLatLng/', views.getLatLng),
    path('about/', views.about),
    path('homepage/', views.homepage),
    path('home/', views.home),
    path('info/', views.info),
    path('ha', views.ha),
    path('map', views.map),
    path('mainpage', views.mainpage),
]