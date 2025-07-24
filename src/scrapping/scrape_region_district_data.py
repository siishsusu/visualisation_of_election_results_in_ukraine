from src.functions.functions import get_file_hrefs, create_folder, get_name, get_tables_to_csv
import time
import random


def scraping_data_regions_districts_to_files(url, 
                                             base_url, 
                                             final_results_df, 
                                             year=2014, 
                                             first_page_atr={'atr':'a', 'class_name':'a1'},
                                             second_page_atr_name='a2',
                                             third_page_atr={'atr':'p', 'class_name':'p2'},
                                             ind=0):
    all_links = []

    # second pages (regions)
    all_links = get_file_hrefs(link=url, df=final_results_df, 
                               atr=first_page_atr['atr'], 
                               class_name=first_page_atr['class_name'])
    # getting all links to regions pages
    all_links = [f'{base_url}{link}' for link in all_links]


    create_folder(where=f'data/raw/{year}/', new_folder='regions_data')
    create_folder(where=f'data/raw/{year}/regions_data/', new_folder='by_candidate')

    # iterating through all links
    for link in all_links:
        # getting name of candidate from page
        name = get_name(link, atr='a', class_name=second_page_atr_name)
        name = name if name[-1] != '.' else name[:-1]
        # reading table to file
        df = get_tables_to_csv(link=link, where=f'data/raw/{year}/regions_data/{name}.csv', ind=-2)
        
        hrefs = get_file_hrefs(link=link, df=df)
        hrefs = [f'{base_url}{link}' for link in hrefs]
        
        # third pages (districts)
        for href in hrefs:
            create_folder(f'data/raw/{year}/regions_data/by_candidate', name)
            name_inner = get_name(href, 
                                  atr=third_page_atr['atr'], 
                                  class_name=third_page_atr['class_name'], 
                                  ind=ind)
            
            get_tables_to_csv(link=href, 
                            where=f'data/raw/{year}/regions_data/by_candidate/{name}/{name_inner}.csv', ind=-2)
            print(f'{name_inner}.csv created')
            time.sleep(random.uniform(1, 5))
        print(f'{name}.csv created')
        time.sleep(random.uniform(1, 5))
        
    return 'Done'
