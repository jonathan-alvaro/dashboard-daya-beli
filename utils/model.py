import os

from joblib import dump, load


def load_model(model_path):
    return load(model_path)


def load_scaler(scaler_path):
    return load(scaler_path)

def predict_yoy(model_dir, X):
    yoy_model = load_model(os.path.join(model_dir, 'yoy_model.pkl'))
    yoy_scaler = load_scaler(os.path.join(model_dir, 'yoy_scaler.pkl'))

    X = yoy_scaler.transform(X)
    return yoy_model.predict(X)

def predict_qoq(model_dir, X):
    qoq_model = load_model(os.path.join(model_dir, 'qoq_model.pkl'))
    qoq_scaler = load_scaler(os.path.join(model_dir, 'qoq_scaler.pkl'))

    X = qoq_scaler.transform(X)
    return qoq_model.predict(X)