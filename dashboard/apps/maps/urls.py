from unicodedata import name
from django.urls import path
from apps.maps.views import Map, Graph

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('map', Map, name="map"),
    path('graph', Graph, name="graph"),
    #path('dash', views.Dash, name="dash"),
]