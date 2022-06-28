from unicodedata import name
from django.urls import path
from apps.maps.views import Map

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.Map, name="map"),
    #path('dash', views.Dash, name="dash"),
]