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

# Load trained scaler and model
model = load_model(os.path.join(model_dir, 'predictor.pkl'))
scaler = load_scaler(os.path.join(model_dir, 'scaler.pkl'))

# Load QoQ data
qoq_X, qoq_y, qoq_inflation, qoq_timestamps = load_qoq_data(
    os.path.join(data_dir, 'all_merged.csv')
)

# Forecast future data using scaled predictors
qoq_X = scaler.transform(qoq_X)
qoq_preds = model.predict(qoq_X)

# Load YoY data
yoy_X, yoy_y, yoy_inflation, yoy_timestamps = load_yoy_data(
    os.path.join(data_dir, 'yoy_complete.csv')
)

# Import CSS stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Expose flask serve for deployment
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Determine HTML layout
app.layout = html.Div([
    dcc.Dropdown(
        id='menu-dropdown',
        options=[
            {'label': 'Nowcasting Daya Beli', 'value': 'forecast'},
            {'label': 'Ukuran Daya Beli (Ukuran Indeks 10 Komoditas Strategis)', 'value': 'index'},
            {'label': 'Ukuran Daya Beli (Variabel Non-Pangan)', 'value': 'non-food'}
        ],
        value='forecast',
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
        graphs = []

        graphs.append(html.Div(
            plot_prediction_graph_qoq(
                qoq_timestamps, qoq_y, qoq_preds, qoq_inflation, 'Daya Beli QoQ'
            ),
            style={
                'width':'50%'
            }
        ))

        return graphs

    elif selected_menu == 'index':
        return html.Iframe(
            id='map-frame',
            src=os.path.join('assets', 'test_map.html'),
            width='100%',
            height='600'
        )
    elif selected_menu == 'non-food':
        return create_non_food_variable_graphs(yoy_X, yoy_y, yoy_timestamps)

if __name__ == '__main__':
    app.run_server(debug=True)
