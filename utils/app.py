import numpy as np
import pandas as pd

import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html

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
        if col == 'Quarter' or col == 'Tahun':
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
                        'text': '{} vs Daya Beli'.format(graph_name_dict.get(col, col)),
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
    
    prediction = pd.Series(prediction)
    data = pd.Series(data)

    prediction = np.append(data.tail(2).values[0:1], prediction.tail(1).values)
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
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                showlegend=False,
                autosize=True
            )
        ),
        config={
            'displayModeBar': False
        }
    )

def create_nowcasting_tab(
    yoy_X, yoy_y, yoy_preds, yoy_ihk, yoy_national_income, yoy_timestamps
):
    divs = []
    
    yoy_latest_pred = yoy_preds[-1]
    yoy_latest_data = yoy_y.tail(2).values[0]
    yoy_latest_timestamp = yoy_timestamps.tail(1).values[0]
    yoy_change = yoy_latest_pred - yoy_latest_data

    divs.append(html.Div(
        [
            plot_prediction_graph_yoy(
                yoy_timestamps, yoy_y, yoy_preds,
                yoy_ihk, yoy_national_income, 'Daya Beli YoY'
            )

        ], style={
            'width':'100%',
            'backgroundImage':'url("assets/map.png")',
            'backgroundSize':'100%',
            'backgroundPosition':'center',
            'backgroundRepeat':'no-repeat'
        }
    ))

    divs.append(html.Div(
        [
            html.Div(
                [
                    html.P(
                        f"Prediksi Daya Beli YoY {yoy_timestamps.tail(1).values[0]}",
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
                    'alignSelf': 'right',
                    'marginRight':'1%'
                }
            ),
            html.Div(
                [
                    html.P([
                        html.Span(className='dot', id='redDot'),
                        'Daya Beli YoY'
                    ]),
                    html.P([
                        html.Span(className='dot', id='yellowDot'),
                        'Daya Beli YoY Prediksi'
                    ]),
                    html.P([
                        html.Span(className='dot', id='greenDot'),
                        'Perubahan IHK YoY'
                    ]),
                    html.P([
                        html.Span(className='dot', id='blueDot'),
                        'Pendapatan Nasional YoY'
                    ])
                ],
                style={
                    'display':'flex',
                    'alignCOntent':'center',
                    'flexDirection':'column'
                }
            )
        ],
        style={
            'display': 'flex',
            'alignContent':'center',
            'flexDirection':'column',
            'justifyContent':'flex-end'
        }
    ))
    
    return html.Div(
        divs,
        style={
            'width':'100%',
            'display':'flex',
            'flexDirection':'row'
        }
    )

def create_homepage():
    body_text = []

    body_text.append(html.H1(
        'DAYA BELI MASYARAKAT',
        style={
            'textAlign':'center'
        }
    ))

    body_text.append(html.P(
        [
            html.I('Dashboard Daya Beli Masyarakat'),
            ' merupakan sistem pemantauan yang menampilkan ',
            html.I('Nowcasting'),
            ' Daya Beli serta pergerakan indikator daya beli secara ',
            html.I('real time')
        ],
        style={
            'width':'75%',
            'textAlign':'center'
        }
    ))

    main_div = html.Div(
        children=body_text,
        style={
            'backgroundImage':'url("assets/background.png")',
            'backgroundSize':'auto auto',
            'alignItems':'center',
            'justifyContent':'center',
            'flexDirection':'column',
            'display':'flex',
            'height':'100vh',
            'width':'100vw',
            'position':'fixed',
            'top':'0px',
            'bottom':'0px',
            'z-index':'-1'
        }
    )

    return main_div