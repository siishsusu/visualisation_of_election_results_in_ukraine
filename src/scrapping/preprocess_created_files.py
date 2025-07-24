import pandas as pd
import os
from src.functions.functions import get_files_and_folders 


def create_regions_and_districts_files(base_folder_path, 
                                       base_folder_path_for_candidates,
                                       path_to_save):
    # getting list of csv files and folders out of specified folder
    csv_files, folders = get_files_and_folders(base_folder_path=base_folder_path)

    # creating dataframe for scoring all data
    final_df = pd.DataFrame()

    # creating df to store data for each region for candidate
    df_candidate_final = pd.DataFrame()


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
    