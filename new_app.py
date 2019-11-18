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
    # Load QoQ data
    qoq_X, qoq_y, qoq_inflation, qoq_timestamps = load_qoq_data(
        os.path.join(data_dir, 'all_merged.csv')
    )

    # Load YoY data
    yoy_X, yoy_y, yoy_inflation, yoy_timestamps = load_yoy_data(
        os.path.join(data_dir, 'yoy_non_food.csv')
    )

    # # Forecast future data
    qoq_preds = predict_qoq(model_dir, qoq_X)
    yoy_preds = predict_yoy(model_dir, yoy_X)

    if selected_menu == 'forecast':
        divs = []

        qoq_latest_pred = qoq_preds[-1]
        qoq_latest_data = qoq_y.tail(1).values[0]
        qoq_latest_timestamp = qoq_timestamps.tail(1).values[0]
        qoq_change = qoq_latest_pred - qoq_latest_data

        qoq_new_year = int(qoq_latest_timestamp[:4])
        qoq_new_quarter = int(qoq_latest_timestamp[-1]) + 1
        if qoq_new_quarter > 4:
            qoq_new_year += 1
            qoq_new_quarter %= 4
        qoq_new_timestamp = f'{qoq_new_year}-Q{qoq_new_quarter}'

        if qoq_change >= 0:
            qoq_text = f'Naik {round(qoq_change, 2)}%'
            qoq_text_color = 'green'
        else:
            qoq_text = f'Turun {-round(qoq_change, 2)}%'
            qoq_text_color = 'red'

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
                            f"Prediksi Daya Beli QoQ {qoq_new_timestamp}",
                            style={
                                'align-self':'center',
                                'font-size':'1em'
                            }
                        ),
                        html.P(
                            str(round(qoq_preds[-1], 2)) + "%",
                            style={
                                'align-self':'center',
                                'font-size':'5em',
                                'margin':0
                            }
                        )
                    ],
                    style={
                        'display':'flex',
                        'align-content':'center',
                        'flex-direction':'column',
                        'align-self': 'right',
                        'margin-right':'2.5%'
                    }
                ),
                html.Div(
                    [
                        html.P(
                            "Perubahan Daya Beli QoQ",
                            style={
                                'align-self':'center',
                                'font-size':'1em'
                            }
                        ),
                        html.P(
                            str(round(qoq_change, 2)) + "%",
                            style={
                                'align-self':'center',
                                'font-size':'5em',
                                'margin':0
                            }
                        )
                    ],
                    style={
                        'display':'flex',
                        'align-content':'center',
                        'flex-direction':'column',
                        'color': qoq_text_color,
                        'align-self': 'right',
                        'margin-right':'1%'
                    }
                )
            ],
            style={
                'display': 'flex',
                'align-content':'center',
                'flex-direction':'row',
                'justify-content':'flex-end'
            }
        ))

        divs.append(html.Div(
            [
                plot_prediction_graph_qoq(
                    qoq_timestamps, qoq_y, qoq_preds, qoq_inflation, 'Daya Beli QoQ'
                )

            ],
            style={
                'width':'100%'
            }
        ))

        divs.append(html.Div(
            [
                html.Div(
                    [
                        html.P(
                            f"Prediksi Daya Beli YoY {yoy_new_timestamp}",
                            style={
                                'align-self':'center',
                                'font-size':'1em'
                            }
                        ),
                        html.P(
                            str(round(yoy_preds[-1], 2)) + "%",
                            style={
                                'align-self':'center',
                                'font-size':'5em',
                                'margin':0
                            }
                        )
                    ],
                    style={
                        'display':'flex',
                        'align-content':'center',
                        'flex-direction':'column',
                        'align-self': 'right',
                        'margin-right':'2.5%'
                    }
                ),
                html.Div(
                    [
                        html.P(
                            "Perubahan Daya Beli YoY",
                            style={
                                'align-self':'center',
                                'font-size':'1em'
                            }
                        ),
                        html.P(
                            str(round(yoy_change, 2)) + "%",
                            style={
                                'align-self':'center',
                                'font-size':'5em',
                                'margin':0
                            }
                        )
                    ],
                    style={
                        'display':'flex',
                        'align-content':'center',
                        'flex-direction':'column',
                        'color': yoy_text_color,
                        'align-self': 'right',
                        'margin-right':'1%'
                    }
                )
            ],
            style={
                'display': 'flex',
                'align-content':'center',
                'flex-direction':'row',
                'justify-content':'flex-end'
            }
        ))

        divs.append(html.Div(
            [
                plot_prediction_graph_yoy(
                    yoy_timestamps, yoy_y, yoy_preds, yoy_inflation, 'Daya Beli YoY'
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
