import numpy as np
import pandas as pd

import plotly.graph_objects as go
import dash_core_components as dcc

def create_non_food_variable_graphs(predictors, targets, timestamps):
    graphs = []
    
    graph_name_dict = {
        'IKK': 'IKK',
        'Car Sales': 'Penjualan Mobil',
        'Motorcycle Sales': 'Penjualan Motor',
        'Cement Consumption': 'Konsumsi Semen',
        'Exchange Rate': 'Nilai Tukar',
        'Daya Beli RT': 'Daya Beli Rumah Tangga',
        'Retail Growth': 'Pertumbuhan Retail'
    }

    for col in predictors:
        if col == 'Quarter':
            continue
        graph = dcc.Graph(
            figure=go.Figure(
                data = [
                    go.Line(
                        x=timestamps, 
                        y=predictors[col],
                        name=col,
                        yaxis='y2',
                        mode='lines+markers',
                        line={
                            'color':'#FF6961',
                            'width': 3
                        },
                        marker={
                            'size':10
                        }
                    ),
                    go.Line(
                        x=timestamps,
                        y=targets,
                        name='Daya Beli',
                        yaxis='y',
                        mode='lines+markers',
                        line={
                            'color':'#77DD77',
                            'width': 3
                        },
                        marker={
                            'size':10
                        }
                    )
                ], layout= go.Layout(
                    title={
                        'text': '{} vs Daya Beli'.format(graph_name_dict[col]),
                        'xanchor': 'center',
                        'x': 0.5
                    },
                    xaxis={
                        'showgrid':False,
                        'showline':True,
                        'linecolor':'#A9A9A9'
                    },
                    yaxis={
                        'title':{
                            'text':'Change Daya Beli (%)',
                            'font':{
                                'color':'#77DD77'
                            }
                        },
                        'showgrid':False,
                        'gridcolor':'#A9A9A9',
                        'zerolinecolor':'#77DD77',
                        'showgrid':True,
                        'showline':True,
                        'linecolor': '#A9A9A9'

                    },
                    yaxis2={
                        'title':{
                            'text':f'Change {col} (%)',
                            'font':{
                                'color':'#FF6961'
                            }
                        },
                        'side':'right',
                        'overlaying':'y',
                        'showgrid':False,
                        'zerolinecolor':'#FF6961'
                    },font={
                        'color': '#ccdbdc'
                    },
                    paper_bgcolor='#284e66',
                    plot_bgcolor='#284e66',
                    showlegend=True
                )
            ),config={'displayModeBar': False}
        )
        graphs.append(graph)
    
    return graphs

def plot_prediction_graph_yoy(timestamps, data, prediction, ihk, national_income, title):

    pred_quarter = int(timestamps.tail(1).values[0][-1]) + 1
    pred_year = int(timestamps.tail(1).values[0][:4])

    if pred_quarter > 4:
        pred_quarter -= 4
        pred_year += 1

    timestamps[len(timestamps)] = f'{pred_year}-Q{pred_quarter}'
    timestamps = timestamps.apply(lambda x : x[2:])
    timestamps = timestamps.reset_index(drop=True)

    prediction = pd.Series(prediction)
    data = pd.Series(data)

    prediction = np.append(data.tail(1).values, prediction.tail(1).values)
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
                    mode='lines+markers',
                    line={
                        'color':'#FF6961'
                    }
                ),
                go.Line(
                    x=timestamps.tail(2),
                    y=prediction,
                    name='Daya Beli YoY Prediksi',
                    mode='lines+markers',
                    line={
                        'color':'#FDFD96'
                    }
                ),
                go.Line(
                    x=timestamps,
                    y=ihk, 
                    name='Perubahan IHK YoY',
                    mode='lines+markers',
                    line={
                        'color':'#77dd77'
                    }
                ),
                go.Line(
                    x=timestamps,
                    y=national_income,
                    name='Pendapatan Nasional YoY',
                    mode='lines+markers',
                    line={
                        'color':'#ADD8E6'
                    }
                )
            ], layout= go.Layout(
                title={
                    'text': title,
                    'xanchor': 'center',
                    'x': 0.5
                },
                xaxis={
                    'showgrid':False,
                    'showline':True,
                    'linecolor': '#A9A9A9'
                },
                yaxis={
                    'title':{
                        'text':title
                    },
                    'gridcolor':'#A9A9A9',
                    'zerolinecolor':'#A9A9A9',
                    'showgrid':True,
                    'showline':True,
                    'linecolor': '#A9A9A9'
                },
                font={
                    'color': '#ccdbdc'
                },
                plot_bgcolor='#284e66',
                paper_bgcolor='#284e66',
                showlegend=False,
                autosize=True
            )
        ),
        config={
            'displayModeBar': False
        }
    )