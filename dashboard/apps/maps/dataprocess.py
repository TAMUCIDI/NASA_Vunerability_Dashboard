import pandas as pd
import numpy as np
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

def init_AHP_Weight_New(request):
    weight_array = np.zeros((6,6))
    for row in range(6):
        for col in range(6):
            weight_array[row][col] = float(request['AHP_Weight[{}][{}]'.format(row, col)])
    return weight_array

def init_AHP_weight_dict(weightDict, request):
    weightDict['Speed90Weight'] = [float(request['Speedweight[0]']), float(request['Speedweight[1]']), float(request['Speedweight[2]']), float(request['Speedweight[3]']), float(request['Speedweight[4]']), float(request['Speedweight[5]'])]
    weightDict['ShorelineDistWeight'] = [float(request['ShorelineDistWeight[0]']), float(request['ShorelineDistWeight[1]']), float(request['ShorelineDistWeight[2]']), float(request['ShorelineDistWeight[3]']), float(request['ShorelineDistWeight[4]']), float(request['ShorelineDistWeight[5]'])]
    weightDict['MilitaryDistWeight'] = [float(request['MilitaryDistWeight[0]']), float(request['MilitaryDistWeight[1]']), float(request['MilitaryDistWeight[2]']), float(request['MilitaryDistWeight[3]']), float(request['MilitaryDistWeight[4]']), float(request['MilitaryDistWeight[5]'])]
    weightDict['Landing19Weight'] = [float(request['Landing19Weight[0]']), float(request['Landing19Weight[1]']), float(request['Landing19Weight[2]']), float(request['Landing19Weight[3]']), float(request['Landing19Weight[4]']), float(request['Landing19Weight[5]'])]
    weightDict['Landing20Weight'] = [float(request['Landing20Weight[0]']), float(request['Landing20Weight[1]']), float(request['Landing20Weight[2]']), float(request['Landing20Weight[3]']), float(request['Landing20Weight[4]']), float(request['Landing20Weight[5]'])]
    weightDict['Landing21Weight'] = [float(request['Landing21Weight[0]']), float(request['Landing21Weight[1]']), float(request['Landing21Weight[2]']), float(request['Landing21Weight[3]']), float(request['Landing21Weight[4]']), float(request['Landing21Weight[5]'])]
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