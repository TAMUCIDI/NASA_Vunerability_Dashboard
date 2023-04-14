import pandas as pd
import geopandas as gpd
#folium
import folium
#from folium import plugins, Choropleth, Figure, Map, GeoJson, FeatureGroup, LayerControl
import branca.colormap as cm
import os

from apps.maps.dataload import dataLoader

def create_map(file_path_dict, algo_choice, fishing_area_choices, weight_dict):
    cwd = os.path.dirname(os.path.realpath(__file__))
    loader = dataLoader(cwd+file_path_dict['polygon_json'], cwd+file_path_dict['polygon_shp'])

    if algo_choice == "AHP":
        score_gdf, consistent_ratio = loader.get_score_gdf(weight_dict=weight_dict, algo_choice=algo_choice)
    else:
        score_gdf = loader.get_score_gdf(weightDict=weight_dict, algoChoice=algo_choice)
        consistent_ratio = "N/A"
    if len(fishing_area_choices) > 0 and 'ALL' not in fishing_area_choices:
        score_gdf = score_gdf[score_gdf['PORT_GROUP'].isin(fishing_area_choices)]

    folium_map = folium.Map(
        location=[35, -125],
        zoom_start=6,
        width=900,
        height=900
    )

    add_choropleth(folium_map, score_gdf)

    add_mouse_position(folium_map)

    add_layer(cwd+file_path_dict['call_area_shp'], folium_map, 'Call Area', 'blue')

    add_layer(cwd+file_path_dict['protected_area_shp'], folium_map, 'Protected Area', 'green')
    
    folium.LayerControl().add_to(folium_map)

    # Create a folium.Figure object and add the folium_map to it
    figure = folium.Figure()
    folium_map.add_to(figure)
    figure.render() 

    return figure, consistent_ratio

def add_choropleth(folium_map, score_gdf):
    folium.Choropleth(
        geo_data=score_gdf,
        data=pd.DataFrame(score_gdf),
        columns=['OBJECTID', 'score'],
        key_on='feature.properties.OBJECTID',
        fill_color='OrRd',
        name='Wind Energy Suitability Score Choropleth',
        line_weight=0.1,
        highlight=True
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