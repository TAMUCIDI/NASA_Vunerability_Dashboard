from django.shortcuts import render

import logging

from .maps import Map
from .dataload import DataLoader
from .forms import WeightForm

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return render(request, 'maps/index.html')

def Map(request):
    if request.method == 'GET':
        dataLoader = DataLoader()
        folium_figure = dataLoader.create_map()
        weightForm = WeightForm()
        context = {
            "map": folium_figure,
            "weightForm": weightForm,
        }
    elif request.method == 'POST':
        if "WeightSubmit" in request.POST:
            weightForm = WeightForm(request.POST)
            if weightForm.is_valid():
                weightForm = weightForm.cleaned_data

    return render(request, 'maps/plotmap.html', context)