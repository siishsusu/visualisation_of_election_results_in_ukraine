import pandas as pd
import time
import os
import requests
from bs4 import BeautifulSoup


url = 'https://www.cvk.gov.ua/pls/vp2014/wp300pt001f01=702.html'
# f'data/raw/2014/final/final_results_2014.csv'


def create_folder(where, new_folder):
    # if new_folder name not already in directory where
    if new_folder not in os.listdir(where):
        # create new folder
        os.makedirs(f'{where}/{new_folder}')
        # message that folder was created
        print(f'Folder {new_folder} was successfully created ({new_folder in os.listdir(where)})')


def get_table(url, ind=-2):
    # get tables from url
    tables = pd.read_html(url, encoding='cp1251')
    # get table at index
    # experimentally for first table created (final 2014 results) I found index -2
    final_results_df = tables[ind]
    # thats the problem in web page, its tables has 0 1 2... as column names
    # so, I renamed them
    final_results_df.columns = final_results_df.iloc[0]
    final_results_df = final_results_df.iloc[1:] # 0th line - column names, so → delete
    # again column graph does not contain useful information
    final_results_df.drop('Графік', axis=1, inplace=True)

    return final_results_df


def df_to_file(df, file_path):
    df.to_csv(file_path, index=False)


create_folder(where='data/raw/', new_folder='2014')
create_folder(where='data/raw/2014', new_folder='final')

# df_to_file(get_table(url), f'data/raw/2014/final/final_results_2014.csv')