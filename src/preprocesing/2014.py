import pandas as pd
import os


base_data_path = 'data/raw/2014/final/'
data_path = {
    'districts': 'candidate_district.csv',
    'final': 'final_results_2014.csv',
    'regions': 'final_results_by_regions.csv'
}


candidates = {
    'Порошенко П. О.': 'Порошенко Петро Олексійович',
    'Тимошенко Ю. В.': 'Тимошенко Юлія Володимирівна',
    'Ляшко О. В.': 'Ляшко Олег Валерійович',
    'Гриценко А. С.': 'Гриценко Анатолій Степанович',
    'Тігіпко С. Л.': 'Тігіпко Сергій Леонідович',
    'Добкін М. М.': 'Добкін Михайло Маркович',
    'Рабінович В. З.': 'Рабінович Вадим Зіновійович',
    'Богомолець О. В.': 'Богомолець Ольга Вадимівна',
    'Симоненко П. М.': 'Симоненко Петро Миколайович',
    'Тягнибок О. Я.': 'Тягнибок Олег Ярославович',
    'Ярош Д. А.': 'Ярош Дмитро Анатолійович',
    'Гриненко А. В.': 'Гриненко Андрій Вікторович',
    'Коновалюк В. І.': 'Коновалюк Валерій Ілліч',
    'Бойко Ю. А.': 'Бойко Юрій Анатолійович',
    'Маломуж М. Г.': 'Маломуж Микола Григорович',
    'Кузьмін Р. Р.': 'Кузьмін Ренат Равелійович',
    'Куйбіда В. С.': 'Куйбіда Василь Степанович',
    'Клименко О. І.': 'Клименко Олександр Іванович',
    'Цушко В. П.': 'Цушко Василь Петрович',
    'Саранов В. Г.': 'Саранов Володимир Георгійович',
    'Шкіряк З. Н.': 'Шкіряк Зорян Нестрович'
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


# creating folder '2014' for storing preprocessed data
if '2014' not in os.listdir('data/preprocessed'):
    os.makedirs('data/preprocessed/2014')


# saving file to folder 
df_final.to_csv('data/preprocessed/2014/final_2014.csv', index=False)
