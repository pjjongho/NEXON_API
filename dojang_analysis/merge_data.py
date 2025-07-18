# api로 크롤링한 데이터 병합
# key값은 character_name

import pandas as pd

info = pd.read_csv('./data/char_info.csv')
stat = pd.read_csv('./data/stat.csv')
popularity = pd.read_csv('./data/popularity.csv')
dojang = pd.read_csv('./data/dojang.csv')

df = info.merge(stat, on='nickname')\
            .merge(popularity, on='nickname')\
            .merge(dojang, on='nickname')

df.to_csv('./data/merged.csv', index=False)