import os
from sklearn.metrics import mean_squared_error

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html
import pandas as pd
import numpy as np

from utils.model import *
from utils.data import *


# Load trained scaler and model
model = load_model(os.path.join('models', 'predictor.pkl'))
scaler = load_scaler(os.path.join('models', 'scaler.pkl'))

# Load QoQ data
qoq_X, qoq_y, qoq_timestamps = load_qoq_data(
    os.path.join('data', 'all_merged.csv')
)

# Forecast future data using scaled predictors
qoq_X = scaler.transform(qoq_X)
qoq_preds = model.predict(qoq_X)


# Import CSS stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Determine HTML layout
app.layout = html.Div([
    dcc.Dropdown(
        id='menu-dropdown',
        options=[
            {'label': 'Forecast', 'value': 'forecast'},
            {'label': 'Index 10 Komoditas Strategis', 'value': 'index'}
        ],
        style={
            'marginBottom': '1em'
        }
    ),

    html.Div(
        id='content-div'
    )
])


@app.callback(
    Output('content-div', 'children'),
    [Input('menu-dropdown', 'value')]
)
def refresh_content(selected_menu):
    if selected_menu == 'forecast':
        return "Forecast Placeholder"
    elif selected_menu == 'index':
        return html.Iframe(
            id='map-frame',
            src=os.path.join('assets', 'test_map.html'),
            width='100%',
            height='600'
        )

if __name__ == '__main__':
    app.run_server(debug=True)
