from email import message
from time import time

from numpy import tile
import pandas as pd
from apps.maps.models import Maps

# Maps Library Import ---------------------------------------------- #
from django.shortcuts import redirect, render
from django.views.generic import TemplateView 

#folium
import folium
#from folium import plugins, Choropleth, Figure, Map, GeoJson, FeatureGroup, LayerControl
import branca.colormap as cm

from apps.maps.forms import MapForm
from django.http import HttpResponse
from django import forms

import logging
import json
import os

from apps.maps.dataload import dataLoader
from apps.maps.dataprocess import init_input_dict, construct_heatmap_gdf, update_weight_dict

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return HttpResponse("Hello World")

def Map(request):

    weightDict = init_input_dict()

    if request.method == 'POST':
        form = MapForm(request.POST)
        if form.is_valid():
            weightDict = update_weight_dict(weightDict, form.cleaned_data)

    figure = folium.Figure()
    m = folium.Map(
        location=[35, -125],
        zoom_start=6,
        height=900
    )

    #load geometry & data
    cwd = os.path.dirname(os.path.realpath(__file__))
    gjsonFilePath = cwd + "/data/polygons.geojson"
    shpFilePath = cwd + "/data/divided_polygons_SpatialJoin12.shp"
    loader = dataLoader(gjsonFilePath, shpFilePath)

    #score geo data frame
    scoreGeoJson, dataDf = loader.get_score_geoJson(weightDict)
    #choropleth
    folium.Choropleth(
        geo_data=scoreGeoJson,
        data=dataDf,
        columns=['objectId', 'score'],
        key_on='feature.properties.objectId',
        fill_color='OrRd'
    ).add_to(m)

    #polygon Boundry Layer
    '''
    gdf = loader.get_gdf()
    gjson = folium.GeoJson(gdf)
    
    polygonLayer = folium.FeatureGroup(
        name='Polygon Boundry',
        show=True,
    )
    m.add_child(polygonLayer)
    gjson.add_to(polygonLayer)
    '''

    #heatmap Layer
    '''
    heatMap = construct_heatmap_gdf(gdf, weightDict)
    heatMapLayer = folium.FeatureGroup(
        name='Heat Map',
        shoe=True,
    )
    m.add_child(heatMapLayer)
    heatMap.add_to(heatMapLayer)
    '''
    

    formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
    folium.plugins.MousePosition(
        position="topright",
        separator=" | ",
        empty_string="NaN",
        lng_first=True,
        num_digits=20,
        prefix="Coordinates:",
        lat_formatter=formatter,
        lng_formatter=formatter,
    ).add_to(m)

    #add layer control
    folium.LayerControl().add_to(m)

    m.get_root().render()
    m.add_to(figure)
    figure.render()
    form = MapForm()
        #form.fields['coords'].widget = forms.HiddenInput()
    return render(request, 'maps/plotmap.html', {"map": figure, "form" : form})