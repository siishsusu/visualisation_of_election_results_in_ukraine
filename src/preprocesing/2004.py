import pandas as pd
import os


base_data_path = 'data/raw/2004/final/'
data_path = {
    'districts': 'candidate_district.csv',
    'final': 'final_results_2004.csv',
    'regions': 'final_results_by_regions.csv'
}


candidates = {
    'Ющенко В. А.': 'Ющенко Віктор Андрійович',
    'Янукович В. Ф.': 'Янукович Віктор Федорович',
    'Мороз О. О.': 'Мороз Олександр Олександрович',
    'Симоненко П. М.': 'Симоненко Петро Миколайович',
    'Вітренко Н. М.': 'Вітренко Наталія Михайлівна',
    'Кінах А. К.': 'Кінах Анатолій Кирилович',
    'Яковенко О. М.': 'Яковенко Олександр Миколайович',
    'Омельченко О. О.': 'Омельченко Олександр Олександрович',
    'Черновецький Л. М.': 'Черновецький Леонід Миколайович',
    'Корчинський Д. О.': 'Корчинський Дмитро Олександрович',
    'Чорновіл А. В.': 'Чорновіл Андрій В’ячеславович',
    'Грабар М. Ф.': 'Грабар Микола Федорович',
    'Бродський М. Ю.': 'Бродський Михайло Юрійович',
    'Збітнєв Ю. І.': 'Збітнєв Юрій Іванович',
    'Комісаренко С. В.': 'Комісаренко Сергій Васильович',
    'Волга В. О.': 'Волга Василь Олександрович',
    'Бойко Б. Ф.': 'Бойко Богдан Федорович',
    'Ржавський О. М.': 'Ржавський Олександр Миколайович',
    'Рогожинський М. В.': 'Рогожинський Микола Володимирович',
    'Кривобоков В. А.': 'Кривобоков Владислав Анатолійович',
    'Базилюк О. Ф.': 'Базилюк Олександр Філімонович',
    'Душин І. Л.': 'Душин Ігор Леонідович',
    'Козак Р. М.': 'Козак Роман Миколайович',
    'Нечипорук В. П.': 'Нечипорук Володимир Павлович'
}


# final data preprocessing
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
df_final['candidate'] = df_final['candidate'].apply(lambda x: candidates[x])
# print(df_final.columns[df_final.isna().sum() > 0]) →
#   Index([], dtype='object')


# creating folder '2004' for storing preprocessed data
if '2004' not in os.listdir('data/preprocessed'):
    os.makedirs('data/preprocessed/2004')


# saving file to folder 
df_final.to_csv('data/preprocessed/2004/final_2004.csv', index=False)
