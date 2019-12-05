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
                            'text':'Perubahan Daya Beli (%)',
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
                            'text':f'Perubahan {col} (%)',
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
                        "Perubahan daya beli dari 1Q sebelumny",
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

def create_about_page():
    return html.Div([
        html.H2('About'),
        html.H1('DAYA BELI MASYARAKAT'),
        html.P([
                'Daya beli (Purchasing Power) adalah kemampuan masyarakat sebagai konsumen untuk ',
                html.B('membeli barang '),
                'dan/atau jasa yang dibutuhkan. Jonh Maynard Keyness mengatakan bahwa daya ',
                'beli masyarakat dapat menurun atau meningkat, dipengaruhi utamanya oleh ',
                'pendapatan yang diperoleh. Meningkatnya ',
                html.B('pendapatan '),
                'akan mendorong individiu untuk menstimulus keseluruhan permintaan barang/jasa ',
                'yang pada akhirnya menggerakkan perekonomian sehingga ekonomi tetap tumbuh. ',
                'Selain pendapatan, daya beli juga dipengaruhi oleh tingkat kenaikan ',
                'harga-harga barang secara umum (inflasi). Beberapa literatur menunjukkan ',
                'bahwa daya beli juga dipengaruhi oleh ekspektasi pendapatn di masa yang akan ',
                'datang, akumulasi kekayaan, serta tingkat suku bunga. Dalam model Nowcasting ',
                'Daya Beli, tingkat daya beli masyarakat diukur melalui ',
                html.B('beberapa indikator '),
                'seperti Penjualan Retail, Penjualan Motor, Penjualan Mobil, Nilai Tukar, ',
                'Konsumsi Semen, Harga Komoditas Pangan, dll.'
        ]),
        html.H1('HUBUNGAN DAYA BELI DAN INFLASI'),
        html.P([
            'Inflasi ',
            html.B('berpengaruh negatif dan signifikan '),
            'terhadap konsumsi. Apabila terjadi inflasi, harga-harga barang dan jasa ',
            'mengalami kenaikan. Kenaikan harga ini menyebabkan daya beli riil masyarakat ',
            'menjadi turun. Penurunan daya beli ini berdampak pada penurunan konsumsi atas ',
            'barang dan jasa. Tingkat inflasi juga menyebabkan terjadinya efek substitusi ',
            '(Persaulian dkk, 2013). Konsumen akan mengurangi pembelian barang-barang ',
            'yang harganya relatif mahal dan mengalihkan konsumsinya dari barang substitusi. ',
            'Inflasi ',
            html.B('yang tinggi melemahkan daya beli '),
            'masyarakat terutama terhadap produksi dalam negeri yang pada akhirnya akan ',
            'mengurangi kepercayaan masyarakat terhadap mata uang nasional.'
        ])
    ])

def create_methods_page():
    return html.Div(
        [
            html.H1('Methods (untuk prototipe)'),
            html.H2('NowCasting Daya Beli'),
            html.P('Nowcasting daya beli bertujuan untuk memprediksi angka daya beli suatu quarter di tingkat nasional berdasarkan nilai-nilai variabel penjelas (yaitu variabel pangan dan non pangan) pada quarter yang sama. Prediksi dilakukan dengan menggunakan model regresi hasil pembelajaran mesin yang menyatakan pola data dari 20 variabel penjelas yang ada (dari periode Q1 2013 - Q1 2019). Regresi merupakan proses mencari relasi terbaik antara variabel bebas (regressor) X dan variabel terikat (response) Y, menentukan kekuatan relasi tersebut, dan memprediksi nilai response Y dari regressor X (Walpole, 2012). Dalam nowcasting daya beli, daya beli sebagai response (Y) dan 20 variabel penjelas sebagai regressor (X). Nilai daya beli sebagai response didapatkan dari laju pendapatan dikurangi laju IHK atau inflasi.'),
            html.Img(src='assets/system.png'),
            html.P('Model regresi terbaik yang digunakan dalam nowcasting daya beli adalah model Random Forest. Berbeda dengan regresi linier yang menghasilkan persamaan linier untuk memberikan nilai prediksi, model Random Forest terdiri atas sejumlah pohon keputusan sehingga prediksi daya beli berupa nilai rata-rata hasil prediksi dari setiap pohon keputusan (lihat gambar di bawah). Hal ini yang menyebabkan Random Forest termasuk ke dalam ensemble method yang homogen.'),
            html.Img(src='assets/random_forest.png'),
            html.H2('Robustness'),
            html.P('Dalam pengembangan model daya beli, dilakukan eksperimen pembelajaran mesin untuk mendapatkan model terbaik.  Ukuran kinerja yang digunakan untuk membandingkan antar model adalah RMSE (root mean square error) sebagai standar ukuran kinerja prediksi nilai kuantitatif. RMSE merupakan estimator nilai simpangan baku pada distribusi error, yaitu perbedaan antara nilai prediksi dan nilai sebenarnya.'),
            html.Img(src='assets/rmse.png'),
            html.P('Dalam eksperimen, dilakukan pembangunan model dengan variasi teknik pembelajaran mesin, set variabel penjelas yang digunakan, dan cara perhitungan nilai quarter NTP dan IHSG (yaitu nilai akhir quarter atau rata-rata). Pembangunan model menggunakan dataset daya beli yang terdiri atas pasangan 20 nilai variabel penjelas dan nilai daya beli untuk setiap quarter. Dataset daya beli terdiri atas 25 pasangan nilai untuk periode Q1 2013 - Q1 2019. Dataset dibagi 2 menjadi data latih (18 quarter awal), dan data validasi (7 quarter akhir). Tidak ada overlap antara data latih dan data validasi. Dengan menggunakan data validasi, model terbaik didapatkan menggunakan Random Forest dengan menggunakan semua variabel penjelas, dan perhitungan nilai quarter NTP dan IHSG dengan nilai akhir quarter. Model ini memiliki nilai RMSE 1.95 dan koefisien determinasi R2=0.44. Detil nilai prediksi dan nilai daya beli hasil perhitungan untuk periode Q3 2017 sampai dengan Q1 2019 dapat dilihat pada grafik berikut ini.'),
            html.Img(src='assets/graph.png'),
            html.P('Feature importance setiap atribut dinyatakan dengan grafik berikut, yang memperlihatkan data variabel laju harga telur ayam ras sebagai indikator yang paling penting.'),
            html.Img(src='assets/features.png'),
            html.H2('Indeks 10 Komoditas Strategis'),
            html.P('Indeks 10 komoditas strategis bertujuan untuk menampilkan indeks nasional dan indeks setiap propinsi. Indeks dihitung menggunakan metode agregat tertimbang sederhana dengan menggunakan bobot 10 komoditas pangan dari Survei Biaya Hidup Tahun 2012 yang dilakukan oleh Badan Pusat Statistik untuk menghitung angka inflasi IHK Nasional.'),
            html.Img(src='assets/ia.png'),
            html.Img(src='assets/weights.png')
        ],
        style={
            'display':'flex',
            'alignItems':'center',
            'flexFlow':'column'
        }
    )
