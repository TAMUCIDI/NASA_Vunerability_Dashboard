import pandas as pd
from folium.plugins import HeatMap
from apps.maps.data.constants import NORMALIZE_COLUMNS

def init_input_dict():
    return {
        'Speed90Weight':1,
        'ShorelineDistWeight':1,
        'MilitaryDistWeight':1,
        'Landing19Weight':1,
        'Landing20Weight':1,
        'Landing21Weight':1,
    }

def update_weight_dict(weightDict, inputDict):
    #weightDict['fishingArea'] = inputDict['fishingArea']
    weightDict['Speed90Weight'] = inputDict['Speed90']
    weightDict['ShorelineDistWeight'] = inputDict['ShorelineDist']
    weightDict['MilitaryDistWeight'] = inputDict['MilitaryDist']
    weightDict['Landing19Weight'] = inputDict['Landing19']
    weightDict['Landing20Weight'] = inputDict['Landing20']
    weightDict['Landing21Weight'] = inputDict['Landing21']

    return weightDict

def normalize(df):
    #for column in df.columns:
    for column in NORMALIZE_COLUMNS:
        df[column] = (df[column] - df[column].min())/(df[column].max() - df[column].min())
    
    return df

def construct_heatmap_gdf(gdf, weightDict):
    centroid = gdf.to_crs('+proj=cea').centroid.to_crs(gdf.crs)
    x, y = centroid.x, centroid.y
    df = pd.DataFrame(gdf[['Speed_90', 'Mili_Dist', 'Shoreline_Dist', '2019','2020', '2021']])
    dfNorm = normalize(df)
    #weighted score
    score = weightDict['Speed90Weight']*dfNorm['Speed_90'] \
        - weightDict['ShorelineDistWeight'] * dfNorm['Shoreline_Dist'] \
        + weightDict['MilitaryDistWeight'] * dfNorm['Mili_Dist'] \
        - weightDict['Landing19Weight'] * dfNorm['2019'] \
        - weightDict['Landing20Weight'] * dfNorm['2020'] \
        - weightDict['Landing21Weight'] * dfNorm['2021'] \

    #normalize score
    for i,s in enumerate(score):
        score[i] = (score[i] - score.min())/(score.max() - score.min())

    dataDf = []
    for i in range(len(x)):
        dataDf.append([y[i],x[i],score[i]])

    return HeatMap(
        data=dataDf,
        min_opacity=0.2,
        gradient={
            0: 'green',
            1: 'red',
        },
    )