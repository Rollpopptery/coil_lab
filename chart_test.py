import plotly.graph_objects as go
import numpy as np

def generate_data():
    x = np.linspace(-10, 10, 100)
    y = np.linspace(-10, 10, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))
    return X, Y, Z

# colorscale options:
#
#Greys: Grey tones.
#YlOrRd: Yellow to orange to red.
#Viridis: Perceptually uniform scale.
#Plasma: Vibrant, blue-purple scale.
#Inferno: Hot, orange-red scale.
#Magma: Earthy, brown-red scale.
#Cividis: Perceptually uniform, blue-purple scale.
#Blues: Various blue shades.
#Reds: Different red hues.
#Greens: Shading from green.

# Create figure
def configure_plot(x, y, Z):
    fig = go.Figure(data=[go.Surface(z=Z, x=x, y=y, colorscale='Viridis')])
    return fig




# Customize plot
def customize_layout(fig):
    buttons = [
        dict(
            label='Reset',
            method='relayout',
            args=[
                {'scene': {'xaxis': {'autorange': True}, 'yaxis': {'autorange': True}, 'zaxis': {'autorange': True}}}]),
        dict(
            label='Zoom',
            method='relayout',
            args=[{'scene': {'xaxis': {'range': [0, 10]}, 'yaxis': {'range': [0, 10]}, 'zaxis': {'range': [0, 10]}}}])
    ]
    fig.update_layout(
        title='3D Sine Wave',
        scene = dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'),
        width=1000,
        height=800
    )
    return(fig)


x, y, Z = generate_data()

fig = configure_plot(x, y, Z)

fig = customize_layout(fig)

# Show plot
fig.show(block=True)