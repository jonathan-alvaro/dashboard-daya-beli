import pandas as pd


def load_yoy_data(csv_path, num_quarters=12) -> (
    pd.DataFrame, pd.Series, pd.Series, pd.Series, pd.Series
):
    df = pd.read_csv(csv_path)
    df = df.tail(num_quarters)

    timestamps = create_timestamp(df['Tahun'], df['Quarter'])

    national_income = pd.read_csv('data/national_income.csv')
    y = df['Daya Beli Nasional']
    ihk = pd.read_csv('data/ihk.csv')
    X = pd.merge(df, national_income, on=['Tahun', 'Quarter'])
    X = pd.merge(X, ihk, on=['Tahun', 'Quarter'])
    national_income = X['National Income']
    ihk = X['IHK']
    X = X.drop(
        ['Daya Beli Nasional', 'National Income', 'IHK'],
        axis=1
    ).diff()

    X['Quarter'] = df['Quarter']

    X = X.fillna(0)

    return (X, y, ihk, national_income, timestamps)

def create_timestamp(years: pd.Series, quarters: pd.Series) -> pd.Series:
    timestamps = years.apply(str) + '-Q' + quarters.apply(str)
    return timestamps
