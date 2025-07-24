import pandas as pd
import os


base_data_path = 'data/raw/2019/final/'
data_path = {
    'districts': 'candidate_district.csv',
    'final': 'final_results_2019.csv',
    'regions': 'final_results_by_regions.csv'
}


# final data visualization
df_final = pd.read_csv(f'{base_data_path}{data_path["final"]}')
# renaming columns
df_final.columns = ['candidate', 'percent_voters', 'number_voters']
# print(df_final.info()) →
#   percent_voters is already in 'float64'
#   number_voters should be cast as 'int64'
# example of data in column 'number_voters': '5 714 034',
#   so, firstly I'm replacing spaces to nothing
df_final['number_voters'] = df_final['number_voters']\
    .apply(lambda x: int(x.replace(' ', '')))
# print(df_final.info()) →
#   number_voters should be cast as 'int64'
# print(df_final['candidate'].unique())
# print(df_final.columns[df_final.isna().sum() > 0]) →
#   Index([], dtype='object')


# creating folder '2019' for storing preprocessed data
if '2019' not in os.listdir('data/preprocessed'):
    os.makedirs('data/preprocessed/2019')


# saving file to folder 
df_final.to_csv('data/preprocessed/2019/final_2019.csv', index=False)
