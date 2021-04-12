from django.urls import path
from . import views

urlpatterns = [
    path('getLatLng/', views.getLatLng),
    path('home/', views.home),
]