import os

from joblib import dump, load


def load_model(model_path):
    return load(model_path)


def load_scaler(scaler_path):
    return load(scaler_path)
