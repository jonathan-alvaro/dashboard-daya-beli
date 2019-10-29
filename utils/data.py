import pandas as pd


def load_qoq_data(csv_path) -> (pd.DataFrame, pd.Series, pd.Series):
    df = pd.read_csv(csv_path)

    timestamps = create_timestamp(df['Tahun'], df['Quarter'])

    y = df['Daya Beli']
    X = df.drop(
        [
            'Daya Beli', 'Tahun', 'Inflasi(QoQ)',
            'Growth Pendapatan(QoQ)', 'GDP PPP'
        ],
        axis=1
    ).diff().fillna(0)

    return (X, y, timestamps)


def create_timestamp(years: pd.Series, quarters: pd.Series) -> pd.Series:
    timestamps = years.apply(str) + '-Q' + quarters.apply(str)
    return timestamps
