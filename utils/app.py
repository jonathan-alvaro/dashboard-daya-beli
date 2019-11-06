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


def plot_prediction_graph(data, title):
    past_data = data.drop(len(data) - 1)
    prediction = data.tail(2).reset_index(drop=True)

    if prediction['Daya Beli'].tail(1).values[0] < past_data.tail(1)['Daya Beli'].values[0]:
        prediction_line_color = 'red'
    else:
        prediction_line_color = 'green'

    return dcc.Graph(
            figure=go.Figure(
                data = [
                    go.Line(
                        x=past_data['label'], 
                        y=past_data['Daya Beli'],
                        name='Data Lampau',
                        line={
                            'color':'blue'
                        }
                    ),
                    go.Line(
                        x=prediction['label'],
                        y=prediction['Daya Beli'],
                        name='Forecast',
                        line={
                            'color':prediction_line_color
                        }
                    )
                ], layout= go.Layout(
                    title={
                        'text': title,
                        'xanchor': 'center',
                        'x': 0.5
                    },
                    yaxis={
                        'title':{
                            'text':f'{title} Growth for Daya Beli'
                        }
                    },
                    showlegend=True
                )
            )
        )


def prepare_forecast_data(timestamps, y, preds):
    preds = pd.Series(preds)

    data = y.tail(6)
    data = data.append(preds.tail(1)).reset_index(drop=True)

    pred_quarter = int(timestamps.tail(1).values[0][-1]) + 1
    pred_year = int(timestamps.tail(1).values[0][:4])

    if pred_quarter > 4:
        pred_quarter = pred_quarter - 4
        pred_year += 1

    timestamps = timestamps.copy()
    timestamps[len(timestamps)] = f'{pred_year}-Q{pred_quarter}'
    timestamps = timestamps.tail(len(data)).reset_index(drop=True)
    
    data = pd.DataFrame({
        'label': timestamps,
        'Daya Beli': data
    })

    return data