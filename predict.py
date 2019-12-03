import os
import joblib

from utils.data import *
from utils.model import *

data_dir='data'
model_dir='models'

# Load YoY data
yoy_X, yoy_y, yoy_ihk, yoy_national_income, yoy_timestamps = load_yoy_data(
    os.path.join(data_dir, 'yoy_dataset_all.csv')
)

# Forecast future data
yoy_preds = predict_yoy(model_dir, yoy_X)

joblib.dump(
    (yoy_X, yoy_y, yoy_ihk, yoy_national_income, yoy_timestamps, yoy_preds),
    os.path.join(data_dir, 'nowcasting.pkl')
)