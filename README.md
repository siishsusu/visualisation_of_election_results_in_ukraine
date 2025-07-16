# <img src='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExb21qNXUzMjg0dWh1ejNoNm1rczF6eXJjOXpkMWpheDd0eTJvZm93ZSZlcD12MV9zdGlja2Vyc19zZWFyY2gmY3Q9cw/55m7McmQ9tcD26kQ3I/giphy.gif' height=25></img> Elections Predictor
Elections Predictor is a project aimed at forecasting election outcomes based on real-world data. The first phase of the project involves gathering publicly available election-related data through web scraping, which will later be used to analyze and train machine learning models for prediction tasks.

## <img src='https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3dWF2ODFheW8xMXAybzd2ZDA3cnJsZnlwancxaWxxeHAzMTcwcGRuMSZlcD12MV9zdGlja2Vyc19yZWxhdGVkJmN0PXM/eGmNtCi4tkA9B18l3L/giphy.gif' height=25></img> Project Goals
* <img src='https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExd3BjajF3MHIwZnIxcjV3Yjl1eWo4cDdhY3FpdGN0dHJrZGp0aTFxciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/MelhioWPAo6k4Q6BTp/giphy.gif' height=20> Scrape and collect historical and recent election data from reliable sources.

[notebook for web scraping](notebooks/web_scrapping.ipynb)

[notebook for preprocessing files](notebooks/preprocessing.ipynb)

* Data was scraped from: 
    * <img src='https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExd3BjajF3MHIwZnIxcjV3Yjl1eWo4cDdhY3FpdGN0dHJrZGp0aTFxciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/MelhioWPAo6k4Q6BTp/giphy.gif' height=20> [2019](https://www.cvk.gov.ua/pls/vp2019/wp300pt001f01=719.html) | [go to part of readme](#2019)
    * [2014](https://www.cvk.gov.ua/pls/vp2014/wp001.html) | [go to part of readme](#2014) 
    * [2010]() 
    * [2004]() 
    * [1999]()


* Clean and preprocess the data for analysis
* Build machine learning models to predict future election outcomes
* Visualize trends, turnout, and candidate support

## <img src='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXdxdnpjd2Fnbmp3aGVkNngzcW8zc3liZnlzdXBpczM2bWxqYXZzeiZlcD12MV9zdGlja2Vyc19zZWFyY2gmY3Q9cw/lNdz4GzldDzGMGXr2Y/giphy.gif' height=25></img> Data Scraping
### <img src='https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExd3BjajF3MHIwZnIxcjV3Yjl1eWo4cDdhY3FpdGN0dHJrZGp0aTFxciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/MelhioWPAo6k4Q6BTp/giphy.gif' height=25> 2019
1. main page was scrapped to one file: [page](https://www.cvk.gov.ua/pls/vp2019/wp300pt001f01=719.html) → [final_results_2019.csv](data/raw/final_results_2019.csv)
2. there were links for each candidate to their results by regions, so I created folders for each of them
```text
data/
│
└── raw/
    │
    └── 2019/
        │
        ├── Балашов_Геннадій_Вікторович/
        │
        ├── Безсмертний_Роман_Петрович/
        │
        ├── ...
        │
        ├── Шевченко_Ігор_Анатолійович/
        │
        └── Шевченко_Олександр_Леонідович/
```
3. each folder contained of `25 files by regions`.
4. so, my next step was to move them into one file for each candidate. for this I created `by_regions` folder in `2019` folder and it now has `32` files for aech candidate. example:
```text
Округ,"% голосів виборців, поданих за кандидата",Рейтинг,"Кількість виборців, які взяли участь у голосуванні в межах ТВО",% опрацьованих протоколів,Область
88,0.15,17,92 089,100.0,Івано-Франківська область
```
5. also not only folders for districts on each region, but csv files for data `candidate — region`, that was created and stored in `2019` folder
6. for my next step I moved them into one file [final_results_by_regions.csv](data/raw/2019/final_results_by_regions.csv). example:
```text
Регіон,"% голосів виборців, поданих за кандидата",Рейтинг,"Кількість виборців, які взяли участь у голосуванні в межах регіону",% опрацьованих протоколів,Кандидат
м.Київ,0.4,10,1 462 690,100.0,Балашов Геннадій Вікторович
```
7. for my last step I created [candidate_district.csv](data/raw/2019/final/candidate_district.csv) file to store data about results of elections per districts. example:
```text
Округ,"% голосів виборців, поданих за кандидата",Рейтинг,"Кількість виборців, які взяли участь у голосуванні в межах ТВО",% опрацьованих протоколів,Область,Кандидат
88,0.15,17.0,92 089,100.0,Івано-Франківська область,Балашов Геннадій Вікторович
```
8. so, the result of scraping:
    
    * [candidates table](data/raw/2019/final/final_results_2019.csv)
    * [candidate — region results](data/raw/2019/final/final_results_by_regions.csv)
    * [candidate — districts results](data/raw/2019/final/candidate_district.csv)

<!--

<img src='https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExd3BjajF3MHIwZnIxcjV3Yjl1eWo4cDdhY3FpdGN0dHJrZGp0aTFxciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/MelhioWPAo6k4Q6BTp/giphy.gif' height=25>

-->
###  2014
**Python Scripts:**
1. [2014.py](src/scrapping/2014.py)

5. so, the result of scraping:
    
    * [candidates table](data/raw/2014/final/final_results_2014.csv)
###  2010
###  2004
###  1999