from update_monthly_data import *

dfs = load_food_excels('update')
food_df = merge_food_dfs(dfs)

print('Loaded data:')
print(food_df)

food_df = calculate_food_index_col(food_df)
print(food_df.iloc[411])

# print('Calculated index column')
# print(food_df['index'])

# cache = load_cache_data('test/cache.csv')
# print('Cache index:')
# print(cache['index'])

# update_cache(food_df, 'test/cache.csv')
# generate_json_data('test/cache.csv', 'test/data.json')