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

model_dir = 'models'
data_dir = 'data'

# Load trained scaler and model
model = load_model(os.path.join(model_dir, 'predictor.pkl'))
scaler = load_scaler(os.path.join(model_dir, 'scaler.pkl'))

# Load QoQ data
qoq_X, qoq_y, qoq_timestamps = load_qoq_data(
    os.path.join(data_dir, 'all_merged.csv')
)

# Forecast future data using scaled predictors
qoq_X = scaler.transform(qoq_X)
qoq_preds = model.predict(qoq_X)

# Load YoY data
yoy_X, yoy_y, yoy_timestamps = load_yoy_data(
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
            {'label': 'Forecast', 'value': 'forecast'},
            {'label': 'Index 10 Komoditas Strategis', 'value': 'index'},
            {'label': 'Variabel Non-Pangan', 'value': 'non-food'}
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


def create_non_food_variable_graphs(predictors, targets, timestamps):
    graphs = []
    
    for col in predictors:
        graph = dcc.Graph(
            figure=go.Figure(
                data = [
                    go.Line(
                        x=timestamps, 
                        y=predictors[col],
                        name=col
                    ),
                    go.Line(
                        x=timestamps,
                        y=targets,
                        name='Daya Beli'
                    )
                ], layout= go.Layout(
                    title={
                        'text': '{} vs Daya Beli'.format(col),
                        'xanchor': 'center',
                        'x': 0.5
                    },
                    showlegend=True
                )
            )
        )
        graphs.append(graph)
    
    return graphs

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
    elif selected_menu == 'non-food':
        return create_non_food_variable_graphs(yoy_X, yoy_y, yoy_timestamps)

if __name__ == '__main__':
    app.run_server(debug=True)
