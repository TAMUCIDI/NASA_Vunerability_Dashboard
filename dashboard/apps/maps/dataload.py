import geopandas as gpd
import pandas as pd
import numpy as np
import os
from folium import GeoJson
from apps.maps.dataprocess import normalize

cwd = os.path.dirname(os.path.realpath(__file__))
#polygon_geoJson_file_path = cwd + "/data/polygons.geojson"
polygon_geoJson_file_path = cwd + "/data/divided_polygons_SpatialJoin.geojson"
polygon_shapefile_file_path = cwd + "/data/divided_polygons_SpatialJoin12.shp"

class dataLoader():
    geojson_filePath = None
    shapefile_filePath = None
    gdf_geojson = None
    gdf_shapefile = None
    geometry = None
    datasets = None

    def __init__(self, geojson_filePath, shapefile_filePath) -> None:
        self.geojson_filePath = geojson_filePath
        self.shapefile_filePath = shapefile_filePath
        try:
            self.gdf_geojson = gpd.read_file(self.geojson_filePath)
            self.gdf_shapefile = gpd.read_file(self.shapefile_filePath)
        except:
            print("failed to load geoJson file:" + geojson_filePath)

        self.geometry = self.gdf_shapefile.to_crs("EPSG:4326").geometry
        self.datasets = self.gdf_geojson[['OBJECTID', 'Area_Name', 'Speed_90', 'Mili_Dist', 'Shoreline_Dist', '2019','2020', 'NAME', 'PORT_GROUP']]

    def get_geometry(self):
        return self.geometry
    
    def get_dataSet(self):
        return self.datasets

    def get_gdf(self):
        return gpd.GeoDataFrame(
            data=self.datasets,
            geometry=self.geometry,
            crs="EPSG:4326"
        )

    def get_score_geoJson(self, weightDict):
        df = pd.DataFrame(
            self.get_gdf()[['Speed_90', 'Mili_Dist', 'Shoreline_Dist', '2019','2020']]
        )
        dfNorm = normalize(df)

        #weighted score
        score = weightDict['Speed90Weight']*dfNorm['Speed_90'] \
        - weightDict['ShorelineDistWeight'] * dfNorm['Shoreline_Dist'] \
        + weightDict['MilitaryDistWeight'] * dfNorm['Mili_Dist'] \
        - weightDict['Landing19Weight'] * dfNorm['2019']

        for i,s in enumerate(score):
            score[i] = (score[i] - score.min())/(score.max() - score.min())

        #protected area
        protected = self.get_gdf()['Area_Name']

        objectId = np.array(self.datasets['OBJECTID'])
        for index, value in protected.items():
            if value != None:
                score[index] = 0

        dataDf = pd.DataFrame(
            data={
                    'objectId': objectId,
                    'score': score,
                }
        )

        return gpd.GeoDataFrame(
                data=dataDf,
                geometry= self.geometry
                ), dataDf
        