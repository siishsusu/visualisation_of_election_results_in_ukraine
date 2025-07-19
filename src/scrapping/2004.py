from functions import create_folder, get_table, df_to_file
from scrape_region_district_data import scraping_data_regions_districts_to_files
from preprocess_created_files import create_regions_and_districts_files


url = 'https://www.cvk.gov.ua/pls/vp2004/wp300e26d.html'
base_url = 'https://www.cvk.gov.ua/pls/vp2004/'


# (1) creating folders if they do not exist
create_folder(where='data/raw/', new_folder='2004')
create_folder(where='data/raw/2004', new_folder='final')
# → in result I have 2 more folders '2004' - main 
#   and 'final' for storing three final dataframes


# (2) creating file from scraped table
final_results_df = get_table(url)
df_to_file(final_results_df, f'data/raw/2004/final/final_results_2004.csv')
# → in result I have one dataframe written to file 'final_results_2004.csv', that
#   contains of data about candidates and their final results


# (3) scraping data about regions / districts results
scraping_data_regions_districts_to_files(url=url, 
                                         base_url=base_url, 
                                         final_results_df=final_results_df, 
                                         year=2004,
                                         first_page_atr={'atr':'a', 'class_name':'a1small'},
                                         second_page_atr_name='a1',
                                         third_page_atr={'atr':'td', 'class_name':'td2'},
                                         ind=1)
# → in result I have 2 more folders ('regions_data' and 'by_candidate' inside first one) 
#   regions_data: 24 csv files with candidate - regions data and 1 folder 'by_candidate'
#   by_candidate: 24 folders with candidate names
#       each folder has 27 csv files with region — districts election data for each candidate


# (4) preprocessing data for further actions
create_regions_and_districts_files(base_folder_path='data/raw/2004/', 
                                   base_folder_path_for_candidates='data/raw/2004/regions_data/by_candidate/',
                                   path_to_save='data/raw/2004/final/')
# → in result I have 2 csv files
#       final_results_by_regions.csv
#       candidate_district.csv
