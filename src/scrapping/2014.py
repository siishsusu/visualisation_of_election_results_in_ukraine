import pandas as pd
import time
import os
import requests
from bs4 import BeautifulSoup


url = 'https://www.cvk.gov.ua/pls/vp2014/wp300pt001f01=702.html'
base_url = 'https://www.cvk.gov.ua/pls/vp2014/'
base_folder_path = 'data/raw/2014/'
base_folder_path_for_candidates = 'data/raw/2014/regions_data/by_candidate/'
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


def get_soup(link):
    res = requests.get(link)
    soup = BeautifulSoup(res.content, 'html.parser')
    return soup


def get_tables_to_csv(link, where, ind=-2):
    df = get_table(url=link, ind=ind)
    df_to_file(df=df, file_path=where)

    return df

def get_name(link, atr='a', class_name='a2'):
    soup = get_soup(link=link)
    return '_'.join(soup.find_all(atr, {'class': class_name})[0].text.strip().split(' '))


def get_file_hrefs(link, df):
    if 'Кандидат' in df.columns:
        col = 'Кандидат'
        existing_values = df[col].values
    else:
        col = 'Регіон'
        existing_values = df[col].values
    soup = get_soup(link=link)
    return [name['href'] for name in soup.find_all('a', {'class': 'a1'}) 
            if name.text in existing_values]


def scraping_data_regions_districts_to_files(url, base_url, final_results_df):
    all_links = []

    # second pages (regions)
    all_links = get_file_hrefs(link=url, df=final_results_df)
    # getting all links to regions pages
    all_links = [f'{base_url}{link}' for link in all_links]


    create_folder(where='data/raw/2014/', new_folder='regions_data')
    create_folder(where='data/raw/2014/regions_data/', new_folder='by_candidate')

    # iterating through all links
    for link in all_links:
        # getting name of candidate from page
        name = get_name(link)
        print(name)
        # reading table to file
        df = get_tables_to_csv(link=link, where=f'data/raw/2014/regions_data/{name}.csv', ind=-2)
        
        hrefs = get_file_hrefs(link=link, df=df)
        hrefs = [f'{base_url}{link}' for link in hrefs]
        
        # third pages (districts)
        for href in hrefs:
            create_folder('data/raw/2014/regions_data/by_candidate', name)
            name_inner = get_name(href, atr='p', class_name='p2')
            get_tables_to_csv(link=href, 
                            where=f'data/raw/2014/regions_data/by_candidate/{name}/{name_inner}.csv', ind=-2)
            print(f'{name_inner}.csv created')
            time.sleep(1)
        print(f'{name}.csv created')
        time.sleep(2)
        
    return 'Done'


# (1) creating folders if they do not exist
# create_folder(where='data/raw/', new_folder='2014')
# create_folder(where='data/raw/2014', new_folder='final')
# → in result I have 2 more folders '2014' - main and 'final' for storing three final dataframes


# (2) creating file from scraped table
# final_results_df = get_table(url)
# df_to_file(final_results_df, f'data/raw/2014/final/final_results_2014.csv')
# → in result I have one dataframe written to file 'final_results_2014.csv', that
#   contains of data about candidates and their final results


# (3) scraping data about regions / districts results
# scraping_data_regions_districts_to_files(url=url, 
#                                          base_url=base_url, 
#                                          final_results_df=final_results_df)
# → in result I have 2 more folders ('regions_data' and 'by_candidate' inside first one) 
#   regions_data: 21 csv files with candidate - regions data and 1 folder 'by_candidate'
#   by_candidate: 21 folders with candidate names
#       each folder has 25 csv files with region — districts election data for each candidate


# (4) preprocessing data for further actions
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

# creating dataframe for scoring all data
final_df = pd.DataFrame()

# creating df to store data for each region for candidate
df_candidate_final = pd.DataFrame()

# setting folder path to save created dataframe to file
# base_folder_path = data/raw/2014/ 
#                  → data/raw/2014/final
path_to_save = f'{base_folder_path}final/'


# iterating through csv_files list
for file_name in csv_files:
    # folder_name.csv = file_name   →   folder_name = file_name.replace('.csv', '')
    folder_name = file_name.replace('.csv', '')
    
    # getting files from the folder
    files_in_folder = os.listdir(f'{base_folder_path_for_candidates}{folder_name}')

    # iterating through files_in_folder list
    for folder_file in files_in_folder:
        # setting file path
        file_path = f'{base_folder_path_for_candidates}{folder_name}/{folder_file}'
        
        # reading file to df
        df = pd.read_csv(file_path)
        
        # creating region column
        df['Область'] = ' '.join(folder_file.replace('.csv', '').split('_'))
        df['Кандидат'] = ' '.join(folder_name.split('_'))

        # concating with final dataframe
        df_candidate_final = pd.concat([df_candidate_final, df], axis=0)


    # setting file path
    file_path = f'{base_folder_path}regions_data/{file_name}'

    # reading csv file
    df = pd.read_csv(file_path)

    # creating candidate column
    df['Кандидат'] = ' '.join(folder_name.split('_'))

    # concating with final dataframe
    final_df = pd.concat([final_df, df], axis=0)


# saving to file
df_candidate_final.to_csv(f'{path_to_save}candidate_district.csv', index=False)
print('File candidate_district.csv was saved successfully!!!')

# saving to file
final_df.to_csv(f'{path_to_save}final_results_by_regions.csv', index=False)
print('File final_results_by_regions.csv was saved successfully!!!')