from django.shortcuts import render
from apps.maps.forms import WSDMWeightForm, FishingAreaChoiceForm, TopsisWeightForm

import numpy as np
import logging
import os

from apps.maps.dataload import dataLoader
from apps.maps.dataprocess import init_input_dict, Update_AHP_Weight_dict

from .maps import create_map
from .graph import create_graphs


# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return render(request, 'maps/index.html')

def process_post_request(request):
    fishing_area_choices = []
    algo_choice = "MCDM"
    MSDM_Weight = init_input_dict()
    TOPSIS_Weight = init_input_dict()
    AHP_Weight = np.zeros((6,6))

    if 'FishingAreaSubmit' in request.POST:
        fishing_form = FishingAreaChoiceForm(request.POST)
        request.session['fishing_area_choices'] = request.POST
        if fishing_form.is_valid():
            fishing_area_choices = fishing_form.cleaned_data['fishingArea']
    elif 'WSDMWeightSubmit' in request.POST:
        MSDM_Weight_Form = WSDMWeightForm(request.POST)
        request.session['MSDM_weight_form'] = request.POST
        if MSDM_Weight_Form.is_valid():
            MSDM_Weight = MSDM_Weight_Form.cleaned_data
            algo_choice = "MCDM"
    elif 'AHPWeightSubmit' in request.POST:
        request.session['AHP_weight_form'] = request.POST
        AHP_Weight = Update_AHP_Weight_dict(request.POST)
        algo_choice = "AHP"
    elif 'TopsisWeightSubmit' in request.POST:
        request.session['TOPSIS_weight_form'] = request.POST
        TOPSIS_Weight_Form = TopsisWeightForm(request.POST)
        if TOPSIS_Weight_Form.is_valid():
            TOPSIS_Weight = TOPSIS_Weight_Form.cleaned_data
            algo_choice = "TOPSIS"

    return fishing_area_choices, algo_choice, MSDM_Weight, AHP_Weight, TOPSIS_Weight

def Map(request):
    

    if request.method == 'POST':
        # update the weight_dict when the user submits the form
        fishing_area_choices, algo_choice, WSDM_Weight, AHP_Weight, TOPSIS_Weight = process_post_request(request)
    else:
        WSDM_Weight = init_input_dict()
        TOPSIS_Weight = init_input_dict()
        AHP_Weight = np.zeros((6,6))
        fishing_area_choices = []
        algo_choice = "MCDM"
        if 'fishing_area_choices' in request.session:
            fishing_area_choices = request.session['fishing_area_choices']
        if 'MSDM_weight_form' in request.session:
            WSDM_Weight = request.session['MSDM_weight_form']
        if 'AHP_weight_form' in request.session:
            AHP_Weight = request.session['AHP_weight_form']
        if 'TOPSIS_weight_form' in request.session:
            TOPSIS_Weight = request.session['TOPSIS_weight_form']
    
    cwd = os.path.dirname(os.path.realpath(__file__))
    gjson_file_path = cwd + "/data/polygons.geojson"
    shp_file_path = cwd + "/data/divided_polygons_SpatialJoin12.shp"
    loader = dataLoader(gjson_file_path, shp_file_path)

    folium_figure, consistent_ratio = create_map(loader, algo_choice, fishing_area_choices, WSDM_Weight)
    

    context = {
        "map": folium_figure,
        "FishingAreaForm": FishingAreaChoiceForm(),
        "WSDM_WeightForm": WSDMWeightForm(WSDM_Weight) if WSDM_Weight != None else WSDMWeightForm(),
        "AHP_WeightForm": AHP_Weight,
        "TopsisWeightForm": TopsisWeightForm(TOPSIS_Weight) if TOPSIS_Weight != None else TopsisWeightForm(),
        "ConsistencyRatio": consistent_ratio,
    }

    return render(request, 'maps/plotmap.html', context)

def Graph(request):
    cwd = os.path.dirname(os.path.realpath(__file__))
    gjson_file_path = cwd + "/data/polygons.geojson"
    shp_file_path = cwd + "/data/divided_polygons_SpatialJoin12.shp"
    loader = dataLoader(gjson_file_path, shp_file_path)

    fig_wind, fig_mili, fig_shoreline, fig_landing = create_graphs(loader)

    context = {
        "SpeedGraph": fig_wind.to_html(full_html=False, default_height=500, default_width=700),
        "MiliGraph": fig_mili.to_html(full_html=False, default_height=500, default_width=700),
        "ShorelineGraph": fig_shoreline.to_html(full_html=False, default_height=500, default_width=700),
        "LandingLineGraph": fig_landing.to_html(full_html=True, default_height=500, default_width=1000),
    }
    return render(request, 'maps/graph.html', context)