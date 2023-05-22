import pandas as pd
import geopandas as gpd
#folium
import folium
#from folium import plugins, Choropleth, Figure, Map, GeoJson, FeatureGroup, LayerControl
import branca.colormap as cm
import os
from .constants import shapefile_path, census_data_path
from apps.maps.dataload import DataLoader

def create_map():
    # load data
    loader = DataLoader()
    gdf = loader.gdf

    folium_map = folium.Map(
        location=[36.084621, -96.921387], 
        zoom_start=7,
        width=900,
        height=900
    )

    add_choropleth(folium_map, gdf)

    #add_mouse_position(folium_map)
    
    folium.LayerControl().add_to(folium_map)

    # Create a folium.Figure object and add the folium_map to it
    figure = folium.Figure()
    folium_map.add_to(figure)
    figure.render() 

    return figure

def add_choropleth(folium_map, gdf):
    folium.Choropleth(
        geo_data=gdf['geometry'],
        data=gdf.dropna(subset=['Female_Percent'])['Female_Percent'],
        key_on='feature.id',
        fill_color='YlGn',
        name='Female Percentage Choropleth',
        line_weight=0.1,
    ).add_to(folium_map)

def add_mouse_position(folium_map):
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
    ).add_to(folium_map)

def add_layer(shp_file, folium_map, layer_name, color):
    gdf = gpd.read_file(shp_file)
    folium.GeoJson(
        gdf,
        name=layer_name,
        style_function=lambda feature: {
            'fillColor': color,
            'color': color,
            'weight': 1,
            'fillOpacity': 0.1,
        }
    ).add_to(folium_map)