import pandas as pd
import time
import os
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import uniform


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


def get_soup(link, retries=3, sleep_min=1, sleep_max=3):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }
    
    for attempt in range(retries):
        try:
            res = session.get(link, headers=headers, timeout=10)
            if res.status_code == 200:
                soup = BeautifulSoup(res.content, 'html.parser')
                session.close()
                return soup
            else:
                print(f"[{res.status_code}] Error for: {link}")
        except requests.RequestException as e:
            print(f"[Attempt {attempt+1}] Error: {e}")
        sleep(uniform(sleep_min, sleep_max))

    session.close()
    return None 


def get_tables_to_csv(link, where, ind=-2):
    df = get_table(url=link, ind=ind)
    df_to_file(df=df, file_path=where)

    return df

def get_name(link, atr='a', class_name='a2', ind=0):
    soup = get_soup(link=link)
    return '_'.join(soup.find_all(atr, {'class': class_name})[ind].text.strip().split(' '))


def get_file_hrefs(link, df, atr='a', class_name='a1'):
    if 'Кандидат' in df.columns:
        col = 'Кандидат'
        existing_values = df[col].values
    else:
        col = 'Регіон'
        existing_values = df[col].values
    soup = get_soup(link=link)
    return [name['href'] for name in soup.find_all(atr, {'class': class_name}) 
            if name.text in existing_values]


def get_files_and_folders(base_folder_path):
    # getting files / folders from directory of 2019'th selection
    last_data = os.listdir(base_folder_path) # ['final', 'regions_data']

    # base_folder_path = data/raw/2014/ → data/raw/2014/regions_data
    last_data = os.listdir(f'{base_folder_path}regions_data')
    # ['by_candidate', 'Богомолець_Ольга_Вадимівна.csv', ... 'Ярош_Дмитро_Анатолійович.csv']

    # getting csv files
    csv_files = [file for file in last_data if '.csv' in file]
    # 'Богомолець_Ольга_Вадимівна.csv', ... 'Ярош_Дмитро_Анатолійович.csv'

    # getting folders
    # base_folder_path = data/raw/2014/ 
    #                  → data/raw/2014/regions_data 
    #                  → data/raw/2014/regions_data/by_candidate
    folders = os.listdir(f'{base_folder_path}regions_data/by_candidate')
    # filtering files from folder name (in case there were some)
    folders = [folder for folder in folders if '.csv' not in folder]
    
    return csv_files, folders

