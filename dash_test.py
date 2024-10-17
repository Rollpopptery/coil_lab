#
# -----** Coil Lab **-----
# wombatpi.net
# Heat map to visualise pulse-shape vs target distance
#
# Modified 17-Oct-2024
#
#


import dash
from dash import dcc, html
from dash.dependencies import Input,  Output, State
import plotly.graph_objects as go
import numpy as np
import random

# Initial data
x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id='plot', figure=go.Figure(data=[go.Heatmap(z=Z, x=x, y=y, colorscale='Viridis')]),
        style = {'height': '800px', 'width': '800px'}
    ),
    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)
])

@app.callback(
    Output('plot', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_plot(n):
    global X, Y, Z

    # Update single point with random value
    x_idx = random.randint(0, 99)
    y_idx = random.randint(0, 99)
    X[x_idx, y_idx] = random.uniform(-10, 10)
    Y[x_idx, y_idx] = random.uniform(-10, 10)
    Z[x_idx, y_idx] = random.uniform(-1, 1)

    fig = go.Figure(data=[go.Heatmap(z=Z, x=x, y=y, colorscale='Viridis')])
    fig.update_layout(uirevision=n)  # Preserve view
    return fig

if __name__ == '__main__':
    app.run_server()