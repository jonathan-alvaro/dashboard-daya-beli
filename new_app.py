import os
from sklearn.metrics import mean_squared_error

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html
import pandas as pd
import numpy as np

from utils.app import *
from utils.model import *
from utils.data import *

model_dir = 'models'
data_dir = 'data'

# Import CSS stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Expose flask serve for deployment
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.css.append_css({'external_url': 'reset.css'})
server = app.server

# Load YoY data
yoy_X, yoy_y, yoy_ihk, yoy_national_income, yoy_timestamps = load_yoy_data(
    os.path.join(data_dir, 'yoy_dataset_all.csv')
)

# Forecast future data
yoy_preds = predict_yoy(model_dir, yoy_X)

# Determine HTML layout
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(
            label='Nowcasting Daya Beli',
            children=[
                create_nowcasting_tab(
                    yoy_X, yoy_y, yoy_preds, yoy_ihk, yoy_national_income, yoy_timestamps
                )
            ]
        ),
        dcc.Tab(
            label='Ukuran Daya Beli (Ukuran Indeks 10 Komoditas Strategis)',
            children = [
                html.Iframe(
                id='map-frame',
                src=os.path.join('assets', 'test_map.html'),
                width='100%',
                height='600'
            )]
        ),
        dcc.Tab(
            label='Ukuran Daya Beli (Komoditas Non-Pangan)',
            children=create_non_food_variable_graphs(yoy_X, yoy_y, yoy_timestamps)
        )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
