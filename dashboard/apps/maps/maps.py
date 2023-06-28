import pandas as pd
import geopandas as gpd
#folium
import folium
#from folium import plugins, Choropleth, Figure, Map, GeoJson, FeatureGroup, LayerControl
import os
from .constants import shapefile_path, census_data_path

class Map():
    def __init__(self, gdf) -> None:
        self.gdf = gdf
        self.map = None
        self.figure = None

    def create_map(self, attribute_name="Female_Percent"):
        self.map = folium.Map(
            location=[35.45, -97.5], 
            zoom_start=10,
            width=900,
            height=900
        )
        add_choropleth(self.map, self.gdf, attribute_name)
        folium.LayerControl().add_to(self.map)
        self.figure = folium.Figure()
        self.map.add_to(self.figure)
        self.figure.render()
        return self.figure

def add_choropleth(folium_map, gdf, attribute_name):
    folium.Choropleth(
        geo_data=gdf['geometry'],
        data=gdf.dropna(subset=[attribute_name])[attribute_name],
        key_on='feature.id',
        fill_color='YlGn',
        name=attribute_name+'Choropleth',
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