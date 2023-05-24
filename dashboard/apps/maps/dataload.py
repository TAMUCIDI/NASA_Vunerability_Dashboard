import geopandas as gpd
import pandas as pd
import numpy as np
from folium import GeoJson
from .constants import shapefile_path, census_data_path, criterion_list
from .maps import Map
from .dataProcess import calculate_vulneral_score
# Data Loader Class
class DataLoader():
    def __init__(self, shapefile_path=shapefile_path, census_data_path=census_data_path) -> None:
        self.shapefile_path = shapefile_path
        self.census_data_path = census_data_path
        self.census_gdf = None
        self.census_df = None
        self.gdf = None
        self.figure = None
        self.criterion_list = None

        # load shapefile
        try:
            self.census_gdf = gpd.read_file(shapefile_path)
        except:
            print("failed to load shapefile")
            return
        # load census data
        try:
            self.census_df = pd.read_excel(census_data_path, sheet_name="2020AGE")
        except:
            print("failed to load census data")
            return
        
        # clean census data
        self.census_df = self.census_df.drop(self.census_df.index[0])
        # convert ID column to int
        self.census_gdf['GEOID'] = self.census_gdf['GEOID'].astype(int)
        self.census_df['GEOID'] = self.census_df['GEOID'].astype(int)
        # merge census data with shapefile
        try:
            self.gdf = self.census_gdf.merge(self.census_df, on='GEOID', how='inner')
        except:
            print("failed to merge census data with shapefile")
            return
        # rename columns
        self.rename_columns()
        # clean data
        self.clean_data()
    
    def clean_data(self):
        for i in range(self.gdf.shape[0]):
            for j in range(self.gdf.shape[1]):
                item = self.gdf.iloc[i][j]
                if type(item) == str:
                    self.gdf.iat[i, j] = 0.0

    def rename_columns(self):
        try:
            self.gdf = self.gdf[
                [
                    'geometry',
                    'GEOID',
                    'Female%',
                    'Age<5>65%',
                    '>15property%',
                    'nodiploma%',
                    '%livingalone',
                    '%minority',
                    '%unemployment',
                    '%language',
                    '%renthouse',
                    'Novehicle%',
                    '%noinsurance',
                    '%disability',
                    '%computer',
                    '%nointernet',
                    '%nophone',  
                ]
            ]
        except:
            print("failed to filter columns")
            return
        try:
            self.gdf = self.gdf.rename(
                columns={
                    'Female%': 'Female_Percent',
                    'Age<5>65%': 'Elder&Young_Percent',
                    '>15property%': 'Property_Percent',
                    'nodiploma%': 'Low_Educ_Percent',
                    '%livingalone': 'Living_Alone_Percent',
                    '%minority': 'Minority_Percent',
                    '%unemployment': 'Unemployment_Percent',
                    '%language': 'Language_Percent',
                    '%renthouse': 'Rent_Percent',
                    'Novehicle%': 'No_Vehicle_Percent',
                    '%noinsurance': 'No_Insurance_Percent',
                    '%disability': 'Disable_Percent',
                    '%computer': 'Computer_Percent',
                    '%nointernet': 'No_Internet_Percent',
                    '%nophone': 'No_Phone_Percent'
                }
            )
            self.criterion_list = criterion_list
        except:
            print("failed to rename columns")
            return

    def create_map(self, atrribute_name = "Female_Percent"):
        init_map = Map(self.gdf)
        self.figure = init_map.create_map(atrribute_name)
        return self.figure
    def normalize_column(self, df, column_name):
        max_value = df[column_name].max()
        min_value = df[column_name].min()
        lower_bound = 0.01
        upper_bound = 0.99
        df[column_name] = lower_bound + (df[column_name] - min_value) * (upper_bound - lower_bound) / (max_value - min_value)
        return df

    def update_weighted_map(self, weights):
        # create a copy of the dataframe
        gdf = self.gdf.copy()
        # drop the geometry column
        df = pd.DataFrame(gdf.drop(columns=['geometry','GEOID']))
        # convert weights to numpy array
        weights = np.array(weights)
        # calculate the weighted sum
        _,_,weighted_sum = calculate_vulneral_score(df, weights, self.criterion_list)
        # add the weighted sum to the dataframe
        self.gdf['Weighted_Sum'] = weighted_sum
        # normalize the weighted sum
        self.gdf = self.normalize_column(self.gdf, 'Weighted_Sum')
        # create a new map
        new_map = Map(self.gdf)
        self.figure = new_map.create_map("Weighted_Sum")