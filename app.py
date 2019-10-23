import os
from joblib import dump, load
from sklearn.metrics import mean_squared_error

import dash
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html
import pandas as pd
import numpy as np
from datetime import datetime

def load_model():
    model_path = os.path.join('models', 'predictor.pkl')
    return load(model_path)

def load_scaler():
    scaler_path = os.path.join('models', 'scaler.pkl')
    return load(scaler_path)

def q_ke_tgl(quarter,tahun):
    q = int(quarter)
    t = int(tahun)
    bulan = [None,3,6,9,12]  #1: maret, 2: juni ; 3:sept; 4: des
    int_tgl = [None,31,30,30,31] #kalau nggak, jadi tanggal 1
    str_tgl = str(t) + "-" + str(bulan[q]) +"-" + str(int_tgl[q])
    date_time_obj = datetime.strptime(str_tgl, '%Y-%m-%d')
    return date_time_obj

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = []
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

model = load_model()
scaler = load_scaler()
prediction_data = pd.read_csv(os.path.join('data', 'all_merged.csv'))

label_df = prediction_data.copy()[['Tahun', 'Quarter']]
label_df['label'] = (
    label_df['Tahun'].apply(str) + '-Q' + label_df['Quarter'].apply(str)
)
label_df = label_df.drop(['Tahun', 'Quarter'], axis=1)
label_df = label_df.shift(-1)
label_df['label'] = label_df['label'].fillna('2019-Q2')
prediction_data.drop(
    ['Inflasi(QoQ)', 'Growth Pendapatan(QoQ)', 'Tahun', 'GDP PPP'],
    axis=1,
    inplace=True
)

y = prediction_data['Daya Beli'].values
x = prediction_data.drop('Daya Beli', axis=1)
x = x.diff().fillna(0)
x = scaler.transform(x)

preds = model.predict(x)
print(label_df)
print('----------------------------------')
print(x)
print('----------------------------------')
print(y)
print('----------------------------------')
print(preds)

df_qoq = pd.read_csv("https://gist.githubusercontent.com/yudiwbs/ed50c1de101f2d0ebaf118540d6c2656/raw/0039e7093fc0ce3356af7ca5e6991d6f8a05d6e3/daya_beli_qoq.csv")
df_pred_qoq = df_qoq.tail(1)
tgl = pd.to_datetime('30-06-2019', format='%d-%m-%Y')
df_pred_qoq = df_pred_qoq.append({'quarter-tahun':tgl, 'daya_beli' : -2}, ignore_index=True)

inflation_qoq = pd.read_csv("https://gist.githubusercontent.com/jonathan-alvaro/52e096ea9d7decd128988bed72aa9cfb/raw/bb5085f1a6f9a3da5da2598aac695914732acd47/qoq.csv")

df_yoy = pd.read_csv("https://gist.githubusercontent.com/yudiwbs/a447d01c52b359502147af679ca5f6f6/raw/c5d7677122594a5d1b10ff5f56a855a5d2d859b8/gistfile1.txt")
df_yoy["quarter-tahun"] =  df_yoy.apply(lambda row: q_ke_tgl(row['Quarter'],row['Tahun']), axis=1)
df_pred_yoy = df_yoy.tail(1) #nanti diganti!!
tgl = pd.to_datetime('30-06-2019', format='%d-%m-%Y')
df_pred_yoy = df_pred_yoy.append({'quarter-tahun':tgl,'Daya Beli Nasional' : -1}, ignore_index=True)



df_motor_yoy = pd.read_csv("https://gist.githubusercontent.com/yudiwbs/475dddbf88b9aa70ea5283e990b83cf7/raw/056a5152f06098e2c4d82cba83188946896e02f4/motor_yoy_qt")

df_telur_yoy = pd.read_csv("https://gist.githubusercontent.com/yudiwbs/f0238a2bfde15d95e8c15920d428c6f6/raw/fd256199b46ae00ae9a6475129283d4c05086faa/telur_yoy.csv")
df_telur_yoy["quarter-tahun"] =  df_motor_yoy.apply(lambda row: q_ke_tgl(row['quarter'],row['tahun']), axis=1)

df_ihk_gdp = pd.read_csv("https://gist.githubusercontent.com/yudiwbs/1dfe3ce1c60d95c7c95d518810aff2f8/raw/ea9e85e49e9326d83125e41da8488ee4671d206e/ihk_gdp.csv")
df_ihk_gdp["quarter-tahun"] =  df_ihk_gdp.apply(lambda row: q_ke_tgl(row['quarter'],row['tahun']), axis=1)

colors = {
#    'background': '#111111',
    'text': '#4287f5',
    'text_pred':'#000000'
}
#style={'backgroundColor': colors['background']}
x2 = np.arange(10)
app.layout = html.Div( children=[
    html.H1(children='Sistem Peringatan Dini Daya Beli',style={'textAlign': 'center','color': colors['text']}),
    html.Div([
        dcc.Tabs(id="tabs", children=[
            dcc.Tab(label='Daya Beli', children=[
                html.Div([
                    html.Div([
                        dcc.Graph(
                            id='dbeli-qoq-graph',
                            figure={
                                'data': [
                                    go.Scatter(
                                       x= df_qoq["quarter-tahun"],
                                       y= df_qoq["daya_beli"],
                                       mode='lines+markers',
                                       name='Daya Beli QoQ'
                                    ),
                                    go.Scatter(
                                        x=df_pred_qoq["quarter-tahun"],
                                        y=df_pred_qoq["daya_beli"],
                                        mode='lines+markers',
                                        name='Daya Beli QoQ Prediksi'
                                    ),
                                    go.Scatter(
                                        x=df_qoq["quarter-tahun"],
                                        y=inflation_qoq["Inflasi(QoQ)"],
                                        mode='lines+markers',
                                        name='Inflasi QoQ'
                                    )
                                ],
                                'layout': {
                                    'title': 'Daya Beli QoQ',
                                    'font': {
                                        'color': colors['text']
                                    }
                                }
                            }
                        ),
                        html.H3(children='Prediksi (Q2 2019): -2.00',style={'textAlign': 'Center','color': colors['text_pred']}),
                        html.P("Penjelasan: Prediksi diperoleh berdasarkan peningkatan penjualan motor (0.4) dan daging (0.5) dan penurunan harga bawang (0.2)", style={'padding': '5px 10px 5px 10px'})
                        ],style={'width': '45%', 'verticalAlign':'top', 'display': 'inline-block', 'margin': '0px 0px 5px 0px', 'border': '1px solid #000'}),

                    html.Div([
                        dcc.Graph(
                            id='dbeli-yoy-graph',
                            figure={
                                'data': [
                                    go.Scatter(
                                       x= df_yoy["quarter-tahun"],
                                       y= df_yoy["Daya Beli Nasional"],
                                       mode='lines+markers',
                                       name='Daya Beli YoY'
                                    ),
                                    go.Scatter(
                                        x=df_pred_yoy["quarter-tahun"],
                                        y=df_pred_yoy["Daya Beli Nasional"],
                                        mode='lines+markers',
                                        name='Daya Beli YoY Prediksi'
                                    ),
                                    go.Scatter(
                                        x=df_yoy["quarter-tahun"],
                                        y=df_yoy["Inflation"],
                                        mode='lines+markers',
                                        name='Inflasi YoY'
                                    )
                                ],
                                'layout': {
                                    'title': 'Daya Beli YoY',
                                    'font': {
                                        'color': colors['text']
                                    }
                                }
                            }
                        ),
                        html.H3(children='Prediksi (Q2 2019): -1.00',style={'textAlign': 'Center','color': colors['text_pred']}),
                        html.P("Penjelasan: Prediksi diperoleh berdasarkan peningkatan harga telur (0.4) dan daging (0.5) dan penurunan harga bawang (0.2)", style={'padding': '5px 10px 5px 10px'})
                    ],style={'width': '45%', 'verticalAlign':'top', 'display': 'inline-block', 'margin': '0px 5px 5px 5px', 'border': '1px solid #000'})
                ])
            ]),
            dcc.Tab(label='Indeks 10 Komoditas', children=[
                html.Iframe(id='map-frame', src='assets/test_map.html', width='100%', height='600')
            ]),
            dcc.Tab(label='Model', children=[
                #==========================================================================================
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                        options=[
                            {'label': 'QoQ', 'value': 'NYC'},
                            {'label': u'YoY', 'value': 'MTL'},
                        ],
                        value='MTL',style={'width': '50%'}
                    ),
                        dcc.Graph(
                            id='ihk-gdp-yoy-graph',
                            figure={
                                'data': [
                                    go.Scatter(
                                       x= label_df['label'],
                                       y=y,
                                       mode='lines+markers',
                                       name='Daya beli sesungguhnya'
                                    ),
                                    go.Scatter(
                                       x= label_df['label'],
                                       y=preds,
                                       mode='lines+markers',
                                       name='Daya beli prediksi'
                                    )
                                ],
                                'layout': {
                                    'title': 'Prediksi vs data (QoQ)',
                                    'font': {
                                        'color': colors['text']
                                    }
                                }
                            }
                        ),
                        ],style={'width': '90%', 'verticalAlign':'top', 'display': 'inline-block', 'margin': '0px 0px 5px 0px', 'border': '1px solid #000'})
                ])
            ])
        ],style={'width': '60%','margin': '50px 0px 0px 0px'})
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)