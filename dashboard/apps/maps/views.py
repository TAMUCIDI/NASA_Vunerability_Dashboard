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
from folium import plugins
import branca.colormap as cm

from apps.maps.forms import MapForm
from django.http import HttpResponse
from django import forms

import logging
import json
import os
from apps.maps.dataload import dataLoader

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return HttpResponse("Hello World")

def init_input_dict():
    return {
        'Speed90Weight':1,
        'ShorelineDistWeight':1,
        'MilitaryDistWeight':1,
        'Landing19Weight':1,
    }

def update_weight_dict(weightDict, inputDict):
    #weightDict['fishingArea'] = inputDict['fishingArea']
    weightDict['Speed90Weight'] = inputDict['Speed90']
    weightDict['ShorelineDistWeight'] = inputDict['ShorelineDist']
    weightDict['MilitaryDistWeight'] = inputDict['MilitaryDist']
    weightDict['Landing19Weight'] = inputDict['Landing19']

    return weightDict

def normalize(df):
    for column in df.columns:
        df[column] = (df[column] - df[column].min())/(df[column].max() - df[column].min())
    
    return df

def construct_heatmap_gdf(gdf, weightDict):
    centroid = gdf.to_crs('+proj=cea').centroid.to_crs(gdf.crs)
    x, y = centroid.x, centroid.y
    df = pd.DataFrame(gdf[['Speed_90', 'Mili_Dist', 'Shoreline_Dist', '2019','2020']])
    dfNorm = normalize(df)
    #weighted score
    score = weightDict['Speed90Weight']*dfNorm['Speed_90'] \
        - weightDict['ShorelineDistWeight'] * dfNorm['Shoreline_Dist'] \
        + weightDict['MilitaryDistWeight'] * dfNorm['Mili_Dist'] \
        - weightDict['Landing19Weight'] * dfNorm['2019']

    #normalize score
    for i,s in enumerate(score):
        score[i] = (score[i] - score.min())/(score.max() - score.min())

    dataDf = []
    for i in range(len(x)):
        dataDf.append([y[i],x[i],score[i]])

    return plugins.HeatMap(
        data=dataDf,
        min_opacity=0.2,
        gradient={
            0: 'green',
            1: 'red',
        },
    )


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

    #polygon Boundry Layer
    gdf = loader.get_gdf()
    gjson = folium.GeoJson(gdf)
    boundryLayer = folium.FeatureGroup(
        name='Polygon Boundry',
        show=True,
    )
    m.add_child(boundryLayer)
    gjson.add_to(boundryLayer)

    #heatmap Layer
    heatMap = construct_heatmap_gdf(gdf, weightDict)
    heatMapLayer = folium.FeatureGroup(
        name='Heat Map',
        shoe=True,
    )
    m.add_child(heatMapLayer)
    heatMap.add_to(heatMapLayer)

    formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
    plugins.MousePosition(
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