from unicodedata import name
from django.urls import path
from apps.maps.views import Map

from . import views

urlpatterns = [
    path('', Map, name='map'),
    path('map', Map, name="map"),
]