#
# -----** Coil Lab **-----
# wombatpi.net
#
# A Line chart displaying signal strength vs sample delay (uSec)

# A Heat map that displays the signal strength as intensity, and the X axis is distance to target
# 'Distance to target' is actually the signal strength at a particular sample..
# the idea is to show the shape of the response vs distance
#
#

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np

import threading
import time
import read_wombat

EXPECTED_DATA_SIZE = 50

x = np.arange(0, 150, 3)
y = np.sin(x)
tempdata = [0] * EXPECTED_DATA_SIZE

heatmap_z = np.random.rand(50, 100)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Graph(id='plot', figure=go.Figure(data=[go.Scatter(x=x, y=y)])),
        dcc.Interval(id='interval-component', interval=500, n_intervals=0)
    ]),
    html.Div([
        dcc.Graph(id='heatmap', figure={}),
        dcc.Interval(id='heatmap-interval', interval=500, n_intervals=0)
    ]),
    html.Div([
        dcc.Interval(id='timer', interval=200, n_intervals=0)
    ]),
    html.Div(id='timer-output', style={'display': 'none'})  # Hidden Div
], style={'display': 'flex', 'flex-direction': 'column'})


@app.callback(
    Output('plot', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_plot(n):
    global tempdata

    fig = go.Figure(data=[go.Scatter(x=x, y=tempdata)])
    return fig


@app.callback(
    Output('heatmap', 'figure'),
    [Input('heatmap-interval', 'n_intervals')]
)
def update_heatmap(n):
    global heatmap_z
    fig = go.Figure(data=go.Heatmap(z=heatmap_z, colorscale='Viridis'))
    return fig


# reading serial data frequently

@app.callback(
    Output('timer-output', 'children'),  # Dummy output
    [Input('timer', 'n_intervals')]
)
def timer_callback(n):
    global tempdata

    with read_wombat.data_lock:
        if len(read_wombat.dataList) == EXPECTED_DATA_SIZE:
            tempdata = read_wombat.dataList.copy()


if __name__ == '__main__':
    read_wombat.runSerial(read_wombat.MODE.SCAN_3USEC)
    app.run_server(debug=False)