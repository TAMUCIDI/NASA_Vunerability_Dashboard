from email import message
from time import time

from numpy import tile
import pandas as pd
import numpy as np
from apps.maps.models import Maps

# Maps Library Import ---------------------------------------------- #
from django.shortcuts import redirect, render
from django.views.generic import TemplateView 

#folium
import folium
#from folium import plugins, Choropleth, Figure, Map, GeoJson, FeatureGroup, LayerControl
import branca.colormap as cm

from apps.maps.forms import MapForm, FishingAreaChoiceForm, TopsisWeightForm
from django.http import HttpResponse
from django import forms

import logging
import json
import os

from apps.maps.dataload import dataLoader
from apps.maps.dataprocess import init_input_dict, construct_heatmap_gdf, update_weight_dict, init_AHP_weight_dict
from apps.maps.data.constants import YEAR_RANGE

from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return HttpResponse("Hello World")

def Map(request):
    #init
    weightDict = init_input_dict()
    topsisWeightDict = init_input_dict()
    fishingAreaChoices = []
    #
    # "MCDM": multi-criteria
    # "AHP"
    # "TOPSIS"
    algoChoice = "MCDM"

    if request.method == 'POST':
        if 'FishingAreaSubmit' in request.POST:
            fishingForm = FishingAreaChoiceForm(request.POST)
            if fishingForm.is_valid():
                fishingAreaChoices = fishingForm.cleaned_data['fishingArea']
        elif 'MapSubmit' in request.POST:
            mapForm = MapForm(request.POST)
            if mapForm.is_valid():
                weightDict = update_weight_dict(weightDict, mapForm.cleaned_data)
                algoChoice = "MCDM"
        elif 'AHPWeightSubmit' in request.POST:
            weightDict = init_AHP_weight_dict(weightDict, request.POST)
            algoChoice = "AHP"
        elif 'TopsisWeightSubmit' in request.POST:
            topsisWeightForm = TopsisWeightForm(request.POST)
            if topsisWeightForm.is_valid():
                topsisWeightDict = update_weight_dict(weightDict, topsisWeightForm.cleaned_data)
                algoChoice = "TOPSIS"

    figure = folium.Figure()
    m = folium.Map(
        location=[35, -125],
        zoom_start=6,
        width=900,
        height=900
    )

    #load geometry & data
    cwd = os.path.dirname(os.path.realpath(__file__))
    gjsonFilePath = cwd + "/data/polygons.geojson"
    shpFilePath = cwd + "/data/divided_polygons_SpatialJoin12.shp"
    loader = dataLoader(gjsonFilePath, shpFilePath)

    #score geo data frame
    #scoreGeoJson, dataDf = loader.get_score_geoJson(weightDict)
    scoreGdf = loader.get_score_gdf(weightDict=weightDict, algoChoice=algoChoice)
    if len(fishingAreaChoices) > 0 and 'ALL' not in fishingAreaChoices:
        scoreGdf = scoreGdf[scoreGdf['PORT_GROUP'].isin(fishingAreaChoices)]
    #choropleth
    folium.Choropleth(
        geo_data=scoreGdf,
        data=pd.DataFrame(scoreGdf),
        columns=['OBJECTID', 'score'],
        key_on='feature.properties.OBJECTID',
        fill_color='OrRd',
        name='Wind Energy Suitability Score Choropleth',
        line_weight=0.1,
        highlight=True
    ).add_to(m)

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
    mapForm = MapForm()
    topsisWeightForm = TopsisWeightForm()
    fishingAreaChoiceForm = FishingAreaChoiceForm()
        #form.fields['coords'].widget = forms.HiddenInput()

    #graph
    df = loader.get_dataSet()

    fig_wind = go.Figure()
    fig_mili = go.Figure()
    fig_shoreline = go.Figure()
    fig_wind.add_trace(go.Box(y=df["Speed_90"], name="All"))
    fig_mili.add_trace(go.Box(y=df["Mili_Dist"], name="All"))
    fig_shoreline.add_trace(go.Box(y=df["Shoreline_Dist"], name="All"))
    for portName, groupData in df.groupby(["NAME"]):
        fig_wind.add_trace(go.Box(y=groupData["Speed_90"], name=portName))
        fig_mili.add_trace(go.Box(y=groupData["Mili_Dist"], name=portName))
        fig_shoreline.add_trace(go.Box(y=groupData["Shoreline_Dist"], name=portName))

    fig_wind.update_layout(
        legend_title_text='Fishing Areas',
        title="Wind speed at 90m statistics grouped by fishing areas",
        xaxis_title="Fishing Area Names",
        yaxis_title="Wind Speed 90m (m/s)"
    )

    fig_mili.update_layout(
        legend_title_text='Fishing Areas',
        title="Distances to military bases statistics grouped by fishing areas",
        xaxis_title="Fishing Area Names",
        yaxis_title="Distance (m)"
    )
    fig_shoreline.update_layout(
        legend_title_text='Fishing Areas',
        title="Distances to shoreline statistics grouped by fishing areas",
        xaxis_title="Fishing Area Names",
        yaxis_title="Distance (m)"
    )

    #landing management line graph
    landingX = YEAR_RANGE
    fig_landing = go.Figure()
    
    landingY = []

    for portName, groupData in df.groupby("NAME"):
        landingY.append(groupData.loc[:, YEAR_RANGE].iloc[0].values)
    landing = np.array(landingY).sum(axis=0)
    fig_landing.add_trace(go.Scatter(x=landingX, y=landing))
    fig_landing.update_layout(
        title="Landing Statistics ", 
        xaxis_title="Year ", 
        yaxis_title="Landing Ammount (mtons")

    SpeedGraph = fig_wind.to_html(full_html=False, default_height=500, default_width=700)
    MiliGraph = fig_mili.to_html(full_html=False, default_height=500, default_width=700)
    ShorelineGraph = fig_shoreline.to_html(full_html=False, default_height=500, default_width=700)
    LandingLineGraph = fig_landing.to_html(full_html=True, default_height=500, default_width=1000)

    context = {
        "map": figure,
        "MapForm": mapForm,
        "FishingAreaForm": fishingAreaChoiceForm,
        "TopsisWeightForm": topsisWeightForm,
        "SpeedGraph": SpeedGraph,
        "MiliGraph": MiliGraph,
        "ShorelineGraph": ShorelineGraph,
        "LandingLineGraph": LandingLineGraph
    }

    return render(request, 'maps/plotmap.html', context)