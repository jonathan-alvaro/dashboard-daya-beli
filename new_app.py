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

    # Load YoY data
    yoy_X, yoy_y, yoy_inflation, yoy_national_income, yoy_timestamps = load_yoy_data(
        os.path.join(data_dir, 'yoy_non_food.csv')
    )
    
    # Forecast future data
    yoy_preds = predict_yoy(model_dir, yoy_X)

    if selected_menu == 'forecast':
        divs = []

        yoy_latest_pred = yoy_preds[-1]
        yoy_latest_data = yoy_y.tail(1).values[0]
        yoy_latest_timestamp = yoy_timestamps.tail(1).values[0]
        yoy_change = yoy_latest_pred - yoy_latest_data

        yoy_new_year = int(yoy_latest_timestamp[:4])
        yoy_new_quarter = int(yoy_latest_timestamp[-1]) + 1
        if yoy_new_quarter > 4:
            yoy_new_year += 1
            yoy_new_quarter %= 4
        yoy_new_timestamp = f'{yoy_new_year}-Q{yoy_new_quarter}'

        if yoy_change >= 0:
            yoy_text = f'Naik {round(yoy_change, 2)}%'
            yoy_text_color = 'green'
        else:
            yoy_text = f'Turun {-round(yoy_change, 2)}%'
            yoy_text_color = 'red'
    
        divs.append(html.Div(
            [
                html.Div(
                    [
                        html.P(
                            f"Prediksi Daya Beli YoY {yoy_new_timestamp}",
                            style={
                                'alignSelf':'center',
                                'fontSize':'1em'
                            }
                        ),
                        html.P(
                            str(round(yoy_preds[-1], 2)) + "%",
                            style={
                                'alignSelf':'center',
                                'fontSize':'5em',
                                'margin':0
                            }
                        )
                    ],
                    style={
                        'display':'flex',
                        'alignContent':'center',
                        'flexDirection':'column',
                        'alignSelf': 'right',
                        'marginRight':'2.5%'
                    }
                ),
                html.Div(
                    [
                        html.P(
                            "Perubahan Daya Beli YoY",
                            style={
                                'alignSelf':'center',
                                'fontSize':'1em'
                            }
                        ),
                        html.P(
                            str(round(yoy_change, 2)) + "%",
                            style={
                                'alignSelf':'center',
                                'fontSize':'5em',
                                'margin':0
                            }
                        )
                    ],
                    style={
                        'display':'flex',
                        'alignContent':'center',
                        'flexDirection':'column',
                        'color': yoy_text_color,
                        'alignSelf': 'right',
                        'marginRight':'1%'
                    }
                )
            ],
            style={
                'display': 'flex',
                'alignContent':'center',
                'flexDirection':'row',
                'justifyContent':'flex-end'
            }
        ))

        divs.append(html.Div(
            [
                plot_prediction_graph_yoy(
                    yoy_timestamps, yoy_y, yoy_preds,
                    yoy_inflation, yoy_national_income, 'Daya Beli YoY'
                )

            ], style={
                'width':'100%'
            }
        ))
        return divs

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
