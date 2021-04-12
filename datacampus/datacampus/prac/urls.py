from django.urls import path
from . import views

urlpatterns = [
    path('getLatLng/', views.getLatLng),
    path('about/', views.about),
    path('homepage/', views.homepage),
    path('home/', views.home),
]