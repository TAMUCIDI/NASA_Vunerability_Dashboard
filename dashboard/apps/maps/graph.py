import numpy as np
from apps.maps.data.constants import YEAR_RANGE
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def create_graphs(loader):
    df = loader.get_dataSet()

    fig_wind = create_wind_graph(df)
    fig_mili = create_mili_graph(df)
    fig_shoreline = create_shoreline_graph(df)
    fig_landing = create_landing_graph(df)

    return fig_wind, fig_mili, fig_shoreline, fig_landing

# Create helper functions for each graph type
#

def create_wind_graph(df):
    fig_wind = go.Figure()

    fig_wind.add_trace(go.Box(y=df["Speed_90"], name="All"))
    for port_name, group_data in df.groupby(["NAME"]):
        fig_wind.add_trace(go.Box(y=group_data["Speed_90"], name=port_name))

    fig_wind.update_layout(
        legend_title_text='Fishing Areas',
        title="Wind speed at 90m statistics grouped by fishing areas",
        xaxis_title="Fishing Area Names",
        yaxis_title="Wind Speed 90m (m/s)"
    )

    return fig_wind

def create_mili_graph(df):
    fig_mili = go.Figure()

    fig_mili.add_trace(go.Box(y=df["Mili_Dist"], name="All"))
    for port_name, group_data in df.groupby(["NAME"]):
        fig_mili.add_trace(go.Box(y=group_data["Mili_Dist"], name=port_name))

    fig_mili.update_layout(
        legend_title_text='Fishing Areas',
        title="Distances to military bases statistics grouped by fishing areas",
        xaxis_title="Fishing Area Names",
        yaxis_title="Distance (m)"
    )

    return fig_mili

def create_shoreline_graph(df):
    fig_shoreline = go.Figure()

    fig_shoreline.add_trace(go.Box(y=df["Shoreline_Dist"], name="All"))
    for port_name, group_data in df.groupby(["NAME"]):
        fig_shoreline.add_trace(go.Box(y=group_data["Shoreline_Dist"], name=port_name))

    fig_shoreline.update_layout(
        legend_title_text='Fishing Areas',
        title="Distances to shoreline statistics grouped by fishing areas",
        xaxis_title="Fishing Area Names",
        yaxis_title="Distance (m)"
    )

    return fig_shoreline

def create_landing_graph(df):
    landing_x = YEAR_RANGE
    fig_landing = go.Figure()

    landing_y = []
    for port_name, group_data in df.groupby("NAME"):
        landing_y.append(group_data.loc[:, YEAR_RANGE].iloc[0].values)
    landing = np.array(landing_y).sum(axis=0)
    fig_landing.add_trace(go.Scatter(x=landing_x, y=landing))
    fig_landing.update_layout(
        title="Landing Statistics",
        xaxis_title="Year",
        yaxis_title="Landing Amount (mtons)"
    )

    return fig_landing