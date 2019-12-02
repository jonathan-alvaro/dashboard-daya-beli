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

# Determine HTML layout
app.layout = html.Div(
    [
        html.Div(
            html.P(
                'Daya Beli Masyarakat',
                style={
                    'font-family':'serif',
                    'fontStyle':'bold'
                }
            ),
            style={
                'float':'left',
                'display':'flex',
                'alignItems':'center',
                'justifyContent':'center',
                'fontSize':'2em'
            }
        ),
        html.Div(
            dcc.Tabs(
                id='dashboard-tabs', value='home',
                children=[
                    dcc.Tab(
                        label='Beranda', value='home',
                        selected_style={
                            'borderBottom':'5px solid #ffc000'
                        }
                    ),
                    dcc.Tab(
                        label='Nowcasting Daya Beli', value='nowcasting',
                        selected_style={
                            'borderBottom':'5px solid #ffc000'
                        }
                    ),
                    dcc.Tab(
                        label='Indikator Daya Beli (Komoditas Pangan)', value='food-index',
                        selected_style={
                            'borderBottom':'5px solid #ffc000'
                        }
                    ),
                    dcc.Tab(
                        label='Indikator Daya Beli (Komoditas Non Pangan)', value='non-food-index',
                        selected_style={
                            'borderBottom':'5px solid #ffc000'
                        }
                    )
                ],
                colors={
                    'background':'transparent'
                }
            ),
            style={
                'width':'50%',
                'float':'right'
            }
        ),
        html.Div(
            id='content',
            style={
                'clear':'both'
            }
        )
    ],
    style={
        'height':'100vh',
        'width':'100%'
    }
)

@app.callback(
    Output('content', 'children'),
    [Input('dashboard-tabs', 'value')]
)
def refresh_content(selected_menu):

    # Load YoY data
    yoy_X, yoy_y, yoy_ihk, yoy_national_income, yoy_timestamps = load_yoy_data(
        os.path.join(data_dir, 'yoy_dataset_all.csv')
    )
    
    # Forecast future data
    yoy_preds = predict_yoy(model_dir, yoy_X)

    if selected_menu == 'home':
        return create_homepage()

    elif selected_menu == 'nowcasting':
        return create_nowcasting_tab(
            yoy_X, yoy_y, yoy_preds, yoy_ihk, yoy_national_income, yoy_timestamps
        )

    elif selected_menu == 'food-index':
        return [html.Iframe(
            id='map-frame',
            src=os.path.join('assets', 'test_map.html'),
            width='100%',
            height='600'
        )]
    elif selected_menu == 'non-food-index':
        return create_non_food_variable_graphs(yoy_X, yoy_y, yoy_timestamps)

if __name__ == '__main__':
    app.run_server(debug=True)
