import pandas as pd


def load_qoq_data(csv_path) -> (pd.DataFrame, pd.Series, pd.Series, pd.Series):
    df = pd.read_csv(csv_path)

    timestamps = create_timestamp(df['Tahun'], df['Quarter'])

    y = df['Daya Beli']
    inflation = df['Inflasi(QoQ)']
    X = df.drop(
        [
            'Daya Beli', 'Tahun', 'Inflasi(QoQ)',
            'Growth Pendapatan(QoQ)', 'GDP PPP'
        ],
        axis=1
    ).diff().fillna(0)

    return (X, y, inflation, timestamps)


def load_yoy_data(csv_path) -> (pd.DataFrame, pd.Series, pd.Series, pd.Series, pd.Series):
    df = pd.read_csv(csv_path)

    timestamps = create_timestamp(df['Tahun'], df['Quarter'])

    national_income = pd.read_csv('data/national_income.csv')
    y = df['Daya Beli Nasional']
    inflation = df['Inflation']
    X = pd.merge(df, national_income, on=['Tahun', 'Quarter'])
    national_income = X['National Income']
    X = X.drop(
        ['Inflation', 'Daya Beli GDP', 'Tahun', 'Daya Beli Nasional', 'National Income'],
        axis=1
    ).diff().fillna(0)

    X['Quarter'] = df['Quarter']

    return (X, y, inflation, national_income, timestamps)

def create_timestamp(years: pd.Series, quarters: pd.Series) -> pd.Series:
    timestamps = years.apply(str) + '-Q' + quarters.apply(str)
    return timestamps
