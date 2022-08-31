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
    gdf_geojson = None
    gdf_shapefile = None
    geometry = None
    datasets = None

    def __init__(self, geojson_filePath, shapefile_filePath) -> None:
        try:
            self.gdf_geojson = gpd.read_file(geojson_filePath)
            self.gdf_shapefile = gpd.read_file(shapefile_filePath)
        except:
            print("failed to load geoJson file:" + geojson_filePath)
            return

        self.geometry = self.gdf_shapefile.to_crs("EPSG:4326").geometry
        self.datasets = self.gdf_geojson[
            [
                'OBJECTID', 
                'Area_Name', 
                'Speed_90', 
                'Mili_Dist', 
                'Shoreline_Dist', 
                '2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020', '2021',
                'NAME', 'PORT_GROUP']]

    def get_geometry(self):
        return self.geometry
    
    def get_dataSet(self):
        return self.datasets

    def get_gdf(self):
        gdf = gpd.GeoDataFrame(
            data=self.datasets,
            geometry=self.geometry,
            crs="EPSG:4326"
        )
        return gdf

    def get_score_gdf(self, weightDict):
        df = pd.DataFrame(
            #self.get_gdf()[['Speed_90', 'Mili_Dist', 'Shoreline_Dist', '2019','2020']]
            self.get_gdf()
        )
        dfNorm = normalize(df)

        #weighted score
        score = weightDict['Speed90Weight']*dfNorm['Speed_90'] \
        - weightDict['ShorelineDistWeight'] * dfNorm['Shoreline_Dist'] \
        + weightDict['MilitaryDistWeight'] * dfNorm['Mili_Dist'] \
        - weightDict['Landing19Weight'] * dfNorm['2019'] \
        - weightDict['Landing20Weight'] * dfNorm['2020'] \
        - weightDict['Landing21Weight'] * dfNorm['2021']

        for i,s in enumerate(score):
            score[i] = (score[i] - score.min())/(score.max() - score.min())

        #protected area
        protected = self.get_gdf()['Area_Name']

        objectId = np.array(self.datasets['OBJECTID'])
        for index, value in protected.items():
            if value != None:
                score[index] = 0

        '''
        dataDf = pd.DataFrame(
            data={
                    'objectId': objectId,
                    'score': score,
                }
        )
        resultGdf = gpd.GeoDataFrame(
            data=dataDf,geometry=self.geometry
        )

        return resultGdf
        '''
        gdf = self.get_gdf()
        gdf['score'] = score

        return gdf