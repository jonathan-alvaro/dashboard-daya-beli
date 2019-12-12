import pandas as pd
import numpy as np
import os
import shutil
from functools import reduce

DB_DATA_PATH = 'database/'
DATASET_PATH = 'yoy_dataset_all.csv'

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def backup(src=DB_DATA_PATH, dst='backup'):
    try:
        copytree(src, dst)
    except OSError:
        print ("Creation of the directory %s failed" % dst)
        return False
    else:
        print ("Successfully backing up database to directory %s " % dst)
        return True

def update_dataset(db_path=DB_DATA_PATH, dataset_path=DATASET_PATH):
    if backup(db_path):
        filenames = os.listdir(db_path)
        all_dataframes = []
        for name in filenames:
            df = pd.read_csv('{}/{}'.format(DB_DATA_PATH, name))
            all_dataframes.append(df)
        merged_data = reduce(
            lambda left, right: pd.merge(left, right, on=['Tahun', 'Quarter'], how='inner'),
            all_dataframes
        )
        cols = merged_data.columns
        cols = cols.drop(['Tahun', 'Quarter', 'Retail Growth'])
        for col in cols:
            merged_data[col] = merged_data[col].pct_change(4) * 100
        merged_data = merged_data.dropna()
        merged_data['Daya Beli Nasional'] = merged_data['Pendapatan Nasional'] - merged_data['IHK']
        merged_data = merged_data.drop(['Pendapatan Nasional', 'IHK'], axis=1)
        merged_data.to_csv(dataset_path, index=False)
        print("Dataset successfully updated")

update_dataset()


