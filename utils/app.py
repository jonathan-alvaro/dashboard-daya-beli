import numpy as np
import pandas as pd

import plotly.graph_objects as go
import dash_core_components as dcc

def create_non_food_variable_graphs(predictors, targets, timestamps):
    graphs = []
    
    for col in predictors:
        graph = dcc.Graph(
            figure=go.Figure(
                data = [
                    go.Line(
                        x=timestamps, 
                        y=predictors[col],
                        name=col,
                        yaxis='y2'
                    ),
                    go.Line(
                        x=timestamps,
                        y=targets,
                        name='Daya Beli',
                        yaxis='y'
                    )
                ], layout= go.Layout(
                    title={
                        'text': '{} vs Daya Beli'.format(col),
                        'xanchor': 'center',
                        'x': 0.5
                    },
                    yaxis={
                        'title':'Change Daya Beli (%)'
                    },
                    yaxis2={
                        'title':f'Change {col} (%)',
                        'side':'right',
                        'overlaying':'y'
                    },
                    showlegend=True
                )
            )
        )
        graphs.append(graph)
    
    return graphs


def plot_prediction_graph_qoq(timestamps, data, prediction, inflation, title):

    pred_quarter = int(timestamps.tail(1).values[0][-1]) + 1
    pred_year = int(timestamps.tail(1).values[0][:4])

    if pred_quarter > 4:
        pred_quarter -= 4
        pred_year += 1

    timestamps[len(timestamps)] = f'{pred_year}-Q{pred_quarter}'
    timestamps = timestamps.reset_index(drop=True)

    prediction = pd.Series(prediction)
    data = pd.Series(data)

    prediction = np.append(data.tail(1).values, prediction.tail(1).values[0])
    prediction = pd.Series(prediction)

    if prediction.tail(1).values[0] < data.tail(1).values[0]:
        prediction_line_color = 'red'
    else:
        prediction_line_color = 'green'

    return dcc.Graph(
        figure=go.Figure(
            data = [
                go.Line(
                    x=timestamps, 
                    y=data,
                    name='Daya Beli QoQ',
                    line={
                        'color':'blue'
                    }
                ),
                go.Line(
                    x=timestamps.tail(2),
                    y=prediction,
                    name='Daya Beli QoQ Prediksi',
                    line={
                        'color':prediction_line_color
                    }
                ),
                go.Line(
                    x=timestamps,
                    y=inflation, 
                    name='Inflasi QoQ'
                )
            ], layout= go.Layout(
                title={
                    'text': title,
                    'xanchor': 'center',
                    'x': 0.5
                },
                yaxis={
                    'title':{
                        'text':title
                    }
                },
                showlegend=True
            )
        )
    )

def plot_prediction_graph_qoq(timestamps, data, prediction, inflation, title):

    pred_quarter = int(timestamps.tail(1).values[0][-1]) + 1
    pred_year = int(timestamps.tail(1).values[0][:4])

    if pred_quarter > 4:
        pred_quarter -= 4
        pred_year += 1

    timestamps[len(timestamps)] = f'{pred_year}-Q{pred_quarter}'
    timestamps = timestamps.reset_index(drop=True)

    prediction = pd.Series(prediction)
    data = pd.Series(data)

    prediction = np.append(data.tail(1).values, prediction.tail(1).values[0])
    prediction = pd.Series(prediction)

    if prediction.tail(1).values[0] < data.tail(1).values[0]:
        prediction_line_color = 'red'
    else:
        prediction_line_color = 'green'

    return dcc.Graph(
        figure=go.Figure(
            data = [
                go.Line(
                    x=timestamps, 
                    y=data,
                    name='Daya Beli YoY',
                    line={
                        'color':'blue'
                    }
                ),
                go.Line(
                    x=timestamps.tail(2),
                    y=prediction,
                    name='Daya Beli YoY Prediksi',
                    line={
                        'color':prediction_line_color
                    }
                ),
                go.Line(
                    x=timestamps,
                    y=inflation, 
                    name='Inflasi YoY'
                )
            ], layout= go.Layout(
                title={
                    'text': title,
                    'xanchor': 'center',
                    'x': 0.5
                },
                yaxis={
                    'title':{
                        'text':title
                    }
                },
                showlegend=True
            )
        )
    )