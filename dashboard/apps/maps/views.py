from django.shortcuts import render

import logging
import os

from .maps import create_map


# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return render(request, 'maps/index.html')

def Map(request):
    
    folium_figure = create_map()

    context = {
        "map": folium_figure,
    }

    return render(request, 'maps/plotmap.html', context)