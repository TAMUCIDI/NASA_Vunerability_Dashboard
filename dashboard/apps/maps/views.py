from django.shortcuts import render
from django.core.cache import cache
import logging
import numpy as np

from .dataload import DataLoader
from .forms import WeightForm, Weight_Default_Dict

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return render(request, 'maps/index.html')

def Map(request):
    # get session key
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    # get cache key
    dataLoaderCacheKey = "dataLoader_" + str(session_key)
    weightsCacheKey = "weights_" + str(session_key)
    if request.method == 'GET':
        # get dataloader
        if cache.has_key(dataLoaderCacheKey):
            dataLoader = cache.get(dataLoaderCacheKey)
        else:
            dataLoader = DataLoader()
            # save dataloader to cache
            cache.set(dataLoaderCacheKey, dataLoader)
        # get weights
        if cache.has_key(weightsCacheKey):
            weightDict = cache.get(weightsCacheKey)
            weightForm = WeightForm(weightDict)
        else:
            weightDict = Weight_Default_Dict
            weightForm = WeightForm(weightDict)
            # save weights to cache
            cache.set(weightsCacheKey, weightDict)
        # get figure
        if not dataLoader.figure:
            #dataLoader.create_map()
            dataLoader.create_map_new()
        folium_figure = dataLoader.figure

    elif request.method == 'POST':
        if "WeightSubmit" in request.POST:
            # get dataloader
            if cache.has_key(dataLoaderCacheKey):
                dataLoader = cache.get(dataLoaderCacheKey)
            else:
                dataLoader = DataLoader()
            # get weights
            weightForm = WeightForm(request.POST)
            if weightForm.is_valid():
                weightDict = weightForm.cleaned_data
                # save weights to cache
                cache.set(weightsCacheKey, weightDict)
                weightList = np.array(list(weightDict.values()))
                # calculate vulnerability score
                #dataLoader.update_weighted_map(weightList)
                dataLoader.update_weighted_map_new(weightList)
                # get updated figure
                folium_figure = dataLoader.figure
        else:
            print("invalid form")
            return render(request, 'maps/index.html')
    context = {
            "map": folium_figure,
            "weightForm": weightForm,
        }
    return render(request, 'maps/plotmap.html', context)