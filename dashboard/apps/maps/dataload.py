import geopandas as gpd
import pandas as pd
import numpy as np
import os
from folium import GeoJson
from pyDecision.algorithm import topsis_method
import ahpy
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

    def get_score_gdf(self, weightDict, algoChoice):
        df = pd.DataFrame(
            #self.get_gdf()[['Speed_90', 'Mili_Dist', 'Shoreline_Dist', '2019','2020']]
            self.get_gdf()
        )
        dfNorm = normalize(df)
        if algoChoice == "MCDM":
            #MCDM weighted score
            score = weightDict['Speed90Weight']*dfNorm['Speed_90'] \
                    - weightDict['ShorelineDistWeight'] * dfNorm['Shoreline_Dist'] \
                    + weightDict['MilitaryDistWeight'] * dfNorm['Mili_Dist'] \
                    - weightDict['Landing19Weight'] * dfNorm['2019'] \
                    - weightDict['Landing20Weight'] * dfNorm['2020'] \
                    - weightDict['Landing21Weight'] * dfNorm['2021']
        elif algoChoice == "TOPSIS":
            #"TOPSIS" weighted score
            topsisWeights = np.array([weightDict['Speed90Weight'], weightDict['ShorelineDistWeight'], weightDict['MilitaryDistWeight'], weightDict['Landing19Weight'], weightDict['Landing20Weight'], weightDict['Landing21Weight']])
            topsisCriterias = ['max', 'min', 'max', 'min', 'min', 'min']
            topsisData = np.array(
                [dfNorm['Speed_90'], dfNorm['Shoreline_Dist'], dfNorm['Mili_Dist'], dfNorm['2019'], dfNorm['2020'], dfNorm['2021']]
            ).T
            score = topsis_method(topsisData, topsisWeights, topsisCriterias, graph=False)
            '''
            topsisDecision = topsis(topsisData, topsisWeights, topsisCriterias)
            topsisDecision.calc()
            score = topsisDecision.C
            '''
        elif algoChoice == "AHP":
            #construct AHP matrix
            feature_list = ['Wind_Speed', 'Shoreline_Distance', 'Military_Distance', '2019_Landing', '2020_Landing', '2021_Landing']
            AHP_feature_len = len(feature_list)
            AHP_Comparison_dict = dict()
            AHPMatrix = [
                weightDict['Speed90Weight'], weightDict['ShorelineDistWeight'], weightDict['MilitaryDistWeight'], weightDict['Landing19Weight'], weightDict['Landing20Weight'], weightDict['Landing21Weight']
            ]

            for i in range(AHP_feature_len):
                for j in range(AHP_feature_len):
                    if i != j:
                        tuple_tmp = (feature_list[i], feature_list[j])
                        AHP_Comparison_dict[tuple_tmp] = AHPMatrix[i][j]
            print(AHP_Comparison_dict)

            #AHP Multi-criteria
            AHP = ahpy.Compare(
                    name='Fishing_Features_AHP', 
                    comparisons=AHP_Comparison_dict, 
                    precision=6, 
                    random_index='saaty')
            AHP_Weights = list(AHP.target_weights.values())
            consistency_ratio = AHP.consistency_ratio
            print(AHP_Weights)

            score = AHP_Weights[0]*dfNorm['Speed_90'] \
                    - AHP_Weights[1] * dfNorm['Shoreline_Dist'] \
                    + AHP_Weights[2] * dfNorm['Mili_Dist'] \
                    - AHP_Weights[3] * dfNorm['2019'] \
                    - AHP_Weights[4] * dfNorm['2020'] \
                    - AHP_Weights[5] * dfNorm['2021']

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
        if algoChoice == "AHP":
            return gdf, consistency_ratio
        else:
            return gdf