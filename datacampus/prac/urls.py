from django.urls import path
from . import views

urlpatterns = [
    path('haha/', views.getLatLng),
]