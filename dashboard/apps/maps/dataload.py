import geopandas as gpd
import os

cwd = os.path.dirname(os.path.realpath(__file__))
polygon_geoJson_file_path = cwd + "/data/polygons.geojson"

class dataLoader():
    filePath = None
    gdf = None

    def __init__(self, filePath) -> None:
        self.filePath = filePath
        try:
            self.gdf = gpd.read_file(self.filePath)
        except:
            print("failed to load geoJson file:" + filePath)

    def get_geometry(self):
        return self.gdf.geometry
    
    def get_gdf(self):
        return self.gdf