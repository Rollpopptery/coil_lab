#
# -----** Coil Lab **-----
# wombatpi.net
# Coil pulse plotting on a line chart
#
# Modified 27-Oct-2024
#
#

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np

import read_wombat
import random

# a way of checking (parsing) the data
EXPECTED_DATA_SIZE = 150

# Initial data
x = np.linspace(0, 10, 100)
y = np.sin(x)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='plot', figure=go.Figure(data=[go.Scatter(x=x, y=y)])),
    dcc.Interval(id='interval-component', interval=1*500, n_intervals=0)
])

@app.callback(
    Output('plot', 'figure'),
    [Input('interval-component', 'n_intervals')]
)

def update_plot(n):
    with read_wombat.data_lock:
        # check we have a valid block of data befor making a copy of it
        if (EXPECTED_DATA_SIZE == len(read_wombat.dataList)):
            tempdata = read_wombat.dataList.copy()

    fig = go.Figure(
        data=[go.Scatter(y=tempdata)],
        layout=go.Layout(
            #height=800,
            title='Wombat Serial Data',
            xaxis_title='Sample Delay (uSec)',
            yaxis_title='Value',
            yaxis=dict(range=[0, 17000])  # Set y-axis range
        )
    )

    fig.update_layout(uirevision=n)  # Preserve view

    return fig

if __name__ == '__main__':
    read_wombat.runSerial(read_wombat.MODE.SCAN_1USEC)
    app.run_server()

