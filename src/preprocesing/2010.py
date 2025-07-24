import pandas as pd
import os


base_data_path = 'data/raw/2010/final/'
data_path = {
    'districts': 'candidate_district.csv',
    'final': 'final_results_2010.csv',
    'regions': 'final_results_by_regions.csv'
}


candidates = {
    'Янукович В. Ф.': 'Янукович Віктор Федорович',
    'Тимошенко Ю. В.': 'Тимошенко Юлія Володимирівна',
    'Тігіпко С. Л.': 'Тігіпко Сергій Леонідович',
    'Яценюк А. П.': 'Яценюк Арсеній Петрович',
    'Ющенко В. А.': 'Ющенко Віктор Андрійович',
    'Симоненко П. М.': 'Симоненко Петро Миколайович',
    'Литвин В. М.': 'Литвин Володимир Михайлович',
    'Тягнибок О. Я.': 'Тягнибок Олег Ярославович',
    'Гриценко А. С.': 'Гриценко Анатолій Степанович',
    'Богословська І. Г.': 'Богословська Інна Германівна',
    'Мороз О. О.': 'Мороз Олександр Олександрович',
    'Костенко Ю. І.': 'Костенко Юрій Іванович',
    'Супрун Л. П.': 'Супрун Людмила Павлівна',
    'Противсіх В. В.': 'Противсіх Василь Васильович',
    'Пабат О. В.': 'Пабат Олександр Вікторович',
    'Ратушняк С. М.': 'Ратушняк Сергій Миколайович',
    'Бродський М. Ю.': 'Бродський Михайло Юрійович',
    'Рябоконь О. В.': 'Рябоконь Олег Васильович'
}


regions_translation = {
    'м.Київ': 'Kyiv',
    'Київська': 'Kyivska',
    'Харківська': 'Kharkivska',
    'Дніпропетровська': 'Dnipropetrovska',
    'Черкаська': 'Cherkaska',
    'Закарпатська': 'Zakarpatska',
    'Рівненська': 'Rivnenska',
    'Одеська': 'Odeska',
    'Полтавська': 'Poltavska',
    'Чернівецька': 'Chernivetska',
    'Хмельницька': 'Khmelnytska',
    'Житомирська': 'Zhytomyrska',
    'Волинська': 'Volynska',
    'Запорізька': 'Zaporizka',
    'Чернігівська': 'Chernihivska',
    'Миколаївська': 'Mykolaivska',
    'Вінницька': 'Vinnytska',
    'Львівська': 'Lvivska',
    'Кіровоградська': 'Kirovohradska',
    'Херсонська': 'Khersonska',
    'Тернопільська': 'Ternopilska',
    'Сумська': 'Sumska',
    'Луганська': 'Luhanska',
    'Івано-Франківська': 'Ivano-Frankivska',
    'Донецька': 'Donetska',
    'Авт.Респ. Крим': 'Avtonomna Respublika Krym',
    'Автономна Республіка Крим': 'Avtonomna Respublika Krym',
    'м.Севастополь': 'Sevastopilska',
}


# -------------- final data preprocessing -------------- 
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


# creating folder '2010' for storing preprocessed data
if '2010' not in os.listdir('data/preprocessed'):
    os.makedirs('data/preprocessed/2010')


# saving file to folder 
df_final.to_csv('data/preprocessed/2010/final_2010.csv', index=False)


# -------------- regions data preprocessing --------------
df_regions = pd.read_csv(f'{base_data_path}{data_path["regions"]}')

# renaming columns
df_regions.columns = ['region', 'percent_votes', 'rating',
       'num_voters_per_region',
       'percent_processed_votes', 'candidate']

#   num_voters_per_region should be cast as 'int64'
# example of data in column 'num_voters_per_region': '1 324 847',
#   so, firstly I'm replacing spaces to nothing
df_regions['num_voters_per_region'] = df_regions['num_voters_per_region']\
    .apply(lambda x: int(x.replace(' ', '')))

# print(df_regions['percent_processed_votes'].unique())
#   [100.]  →   so, I'm dropping this column
df_regions.drop(['percent_processed_votes'], axis=1, inplace=True)

# print(df_regions.columns[df_regions.isna().sum() > 0]) →
#   Index([], dtype='object')

# print(df_regions['region'].unique())

df_regions['candidate'] = df_regions['candidate'].apply(lambda x: candidates[f'{x.replace(".", ". ")}.'])

# creating translated column
df_regions['region_eng'] = df_regions['region'].apply(lambda x: regions_translation[x])

# changing the order of columns
df_regions = df_regions[['candidate', 'region', 'region_eng', 'percent_votes', 'rating', 
                         'num_voters_per_region']]

# saving to file
df_regions.to_csv('data/preprocessed/2010/regions_2010.csv', index=False)


# -------------- districts data preprocessing --------------
df_dist = pd.read_csv(f'{base_data_path}{data_path["districts"]}')
# renaming columns
df_dist.columns = ['district', 'percent_voters_per_candidate', 'rating',
       'number_voters', 'percent_processed_votes', 'region', 'candidate']

# print(df_dist['percent_processed_votes'].unique())
# print(df_regions['percent_processed_votes'].unique())
#   [100.]  →   so, I'm dropping this column
df_dist.drop(['percent_processed_votes'], axis=1, inplace=True)

# print(df_dist['number_voters'].sample(10))
#   number_voters should be cast as 'int64'
# example of data in column 'number_voters': '83 790',
#   so, firstly I'm replacing spaces to nothing
df_dist['number_voters'] =df_dist['number_voters']\
    .apply(lambda x: int(x.replace(' ', '')))

# looking for rows where there is no ' область' in region column
# print(df_dist[~(df_dist['region'].str.contains(' область'))])
#   I see a lot of 'м.Київ', so my next step:
# print(df_dist[~(df_dist['region'].str.contains(' область'))]['region'].unique())
#   ['м.Київ'], so I was right, there are only 'м.Київ' and '(something) область' rows

# deleting ' область' to translate regions
df_dist['region'] = df_dist['region'].apply(lambda x: x.replace(' область', '').strip())

# changing names of candidates to full
df_dist['candidate'] = df_dist['candidate'].apply(lambda x: candidates[f'{x.replace(".", ". ")}.'])

# creating translated column
df_dist['region_eng'] = df_dist['region'].apply(lambda x: regions_translation[x])

# changing the order of columns
df_dist = df_dist[['candidate', 'region', 'region_eng', 'district', 
                   'percent_voters_per_candidate', 'rating', 'number_voters']]

# saving to file
df_regions.to_csv('data/preprocessed/2010/districts_2010.csv', index=False)
