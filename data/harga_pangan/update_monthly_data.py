import datetime
import json
import os
from shutil import copyfile
import time
from functools import reduce

import pandas as pd

def get_variable_names():
    # Define variable names
    variables = [
        'Bawang Merah',
        'Bawang Putih',
        'Beras',
        'Cabai Merah',
        'Cabai Rawit',
        'Daging Ayam',
        'Daging Sapi',
        'Gula Pasir',
        'Minyak Goreng',
        'Telur Ayam'
    ]

    return variables

def get_food_weights():
    # Load aggregated index weights for each food
    weights_csv_path = os.path.join('input', 'food_weight.csv')
    return pd.read_csv(weights_csv_path)

def get_province_id_dict():
    # Load geojson data
    province_json_path = os.path.join('input', 'indonesia-prov.json')
    province_data = json.load(open(province_json_path))['features']

    # Get the ID for every province
    province_ids = {}
    for province in province_data:
        province_properties = province['properties']

        province_name = province_properties['Propinsi'].lower()
        province_ids[province_name] = province_properties['ID']

    # Set special ID for national data
    province_ids['semua provinsi'] = -1
    return province_ids

def get_month_shorthand(month_number):
    shorthand_names = month_dict = {
        '1': 'JAN',
        '2': 'FEB',
        '3': 'MAR',
        '4': 'APR',
        '5': 'MEI',
        '6': 'JUN',
        '7': 'JUL',
        '8': 'AUG',
        '9': 'SEP',
        '10': 'OKT',
        '11': 'NOV',
        '12': 'DES'
    }

    return shorthand_names[str(int(month_number))]

def load_food_data(xlsx_path, food_name):
    # Read data
    df = pd.read_excel(
        xlsx_path
    )

    # Rename columns
    df.columns = ['Tanggal', 'Harga', 'Provinsi']

    # Remove rows where the value is missing
    df = df.loc[
        df['Harga'] != '-'
    ].reset_index(drop=True)
    df['Harga'] = df['Harga'].astype(float)

    # Remove whitespace from province name
    df['Provinsi'] = df['Provinsi'].apply(lambda x: x.strip())

    # Split date into three columns
    df['Bulan'] = pd.to_datetime(df['Tanggal'], format='%d/%m/%Y').apply(lambda x: int(x.month))
    df['Tahun'] = pd.to_datetime(df['Tanggal'], format='%d/%m/%Y').apply(lambda x: int(x.year))
    df['Tanggal'] = pd.to_datetime(df['Tanggal'], format='%d/%m/%Y').apply(lambda x: int(x.day))

    # Sort values by date and province
    df = df.sort_values(
        by=['Tahun', 'Bulan', 'Tanggal', 'Provinsi']
    )

    # Reorder the columns and rename column `Harga` to the variable's name
    df = df[[
        'Tahun', 'Bulan', 'Tanggal', 'Provinsi', 'Harga'
    ]]
    df = df.rename(columns={'Harga': food_name})
    df = df.reset_index(drop=True)

    # Calculate monthly average price
    df = df.groupby(['Tahun', 'Bulan', 'Provinsi']).mean().reset_index()
    df = df.drop('Tanggal', axis=1)

    return df

def load_food_excels(dir_path):
    variables = get_variable_names()

    # Load dataframe for each food variable 
    food_dfs = []
    for name in variables:
        data_path = os.path.join(dir_path, f'{name}.xlsx')
        food_dfs.append(load_food_data(data_path, name))

    return food_dfs

def merge_food_dfs(food_dfs):
    # Merge the dataframes for each food variable into one
    merged_food_df = reduce(pd.merge, food_dfs)
    return merged_food_df

def calculate_prev_month(food_df):
    # Calculate previous month number
    food_df['Prev Bulan'] = food_df.apply(
        lambda row: row['Bulan'] - 1 if row['Bulan'] > 1 else 12, axis=1
    )
    
    # Calculate previous month's year
    food_df['Prev Tahun'] = food_df.apply(
        lambda row:row['Tahun'] if row['Prev Bulan'] != 12 else row['Tahun'] - 1,
        axis=1
    )

    return food_df

def calculate_row_food_index(row, weights):
    # Calculate aggregate MtM index for the row
    Pn = 0
    Po = 0
    for food in pd.unique(weights['food']):
        food_weight = weights.loc[weights['food'] == food]['weight'].values[0]
        Pn += row[food + '_x'] * food_weight
        Po += row[food + '_y'] * food_weight
    
    index = Pn / Po * 100
    return index - 100

def calculate_food_index_col(food_df):
    # Calculate previous month and year for each row
    food_df = calculate_prev_month(food_df)

    # Merge data to get previous month's data on the same row
    food_df = pd.merge(
        food_df, food_df,
        left_on=['Prev Tahun', 'Prev Bulan', 'Provinsi'],
        right_on=['Tahun', 'Bulan', 'Provinsi']
    )

    # Remove merging variables
    food_df = food_df.drop(
        ['Tahun_y', 'Prev Tahun_x', 'Prev Tahun_y', 'Prev Bulan_x', 'Prev Bulan_y'],
        axis=1
    )

    # Calculate aggregative index for each row
    food_index_weight = get_food_weights()
    food_df['index'] = food_df.apply(
        calculate_row_food_index, axis=1, weights=food_index_weight
    )

    # Drop previous month's data
    food_names = get_variable_names()
    columns_to_drop = [name + '_y' for name in food_names]
    food_df = food_df.drop(columns_to_drop, axis=1)

    # Remove _x suffix from column names
    food_df.columns = [
        col[:-2] if col[-2:] == '_x' else col for col in food_df.columns
    ]

    return food_df

def load_cache_data(cache_path):
    # Load cached data
    return pd.read_csv(cache_path)

def backup_cache(cache_path, backup_dir):
    backup_path = os.path.join(backup_dir, f'{datetime.datetime.now()}.csv')
    copyfile(cache_path, backup_path)

def update_cache(new_data, cache_path):
    # Load cache and update with new data
    cache = load_cache_data(cache_path)
    cache = cache.set_index(['Tahun', 'Bulan', 'Provinsi'])
    new_data = new_data.set_index(['Tahun', 'Bulan', 'Provinsi'])
    cache.update(new_data)
    cache = cache.reset_index()
    new_data = new_data.reset_index()
    cache = cache.append(new_data).reset_index(drop=True)
    cache = cache.drop_duplicates()
    cache = cache.sort_values(by=['Tahun', 'Bulan', 'Provinsi'])
    cache['Tahun'] = cache['Tahun'].astype(int)
    cache['Bulan'] = cache['Bulan'].astype(int)

    # Save new cache
    cache.to_csv(cache_path, index=False)

def generate_period_dict(period_data):
    # Create a dictionary of prices for each location
    period_dict = {}
    for location in pd.unique(period_data['Provinsi']):
        location_data = period_data.loc[period_data['Provinsi'] == location]

        location_dict = {}

        food_names = get_variable_names()
        for name in food_names:
            location_dict[name] = float(location_data[name].values[0])
        
        location_dict['index'] = float(location_data['index'].values[0])
        period_dict[str(location)] = location_dict

    return period_dict

def generate_json_data(cache_path, json_path):
    # Load food data from cache
    data = load_cache_data(cache_path)

    # Convert all province names to lowercase and replace with its ID
    province_ids = get_province_id_dict()
    data['Provinsi'] = data['Provinsi'].apply(lambda x : x.lower())
    data['Provinsi'] = data['Provinsi'].replace(province_ids)

    # Convert months from numbers into three letter strings
    data['Bulan'] = data['Bulan'].apply(get_month_shorthand)

    # Create label for json indexing
    data['label'] = data['Bulan'] + '-' + data['Tahun'].apply(str)

    # Create per-province dictionary of prices for each period
    json_dict = {}
    for period in pd.unique(data['label']):
        period_data = data.loc[data['label'] == period].reset_index(drop=True)

        period_dict = generate_period_dict(period_data)
        json_dict[period] = period_dict

    with open(json_path, 'w') as f:
        json.dump(json_dict, f)

dfs = load_food_excels('update')
new_df = merge_food_dfs(dfs)
new_df = calculate_food_index_col(new_df)

backup_cache('update/cache.csv', 'backup/')
update_cache(new_df, 'update/cache.csv')
generate_json_data('update/cache.csv', 'output/data.json')