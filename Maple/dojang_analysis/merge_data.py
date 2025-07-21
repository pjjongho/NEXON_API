# api로 크롤링한 data preprocessing
# key값은 character_name

import pandas as pd
import numpy as np
import ast
import os

# Data preprocessing
# 수집한 데이터 별로 불필요한 컬럼 제거
# stat, dojang은 딕셔너리 컬럼이 존재해서 좀 까다로웠음

def data_processing():

    # data 경로 설정 
    # data가 총 5개 이므로, 공통 경로 설정 후에 로드
    base_path = './data/'

    char_info = pd.read_csv(os.path.join(base_path, 'char_info.csv'))
    dojang = pd.read_csv(os.path.join(base_path, 'dojang.csv'))
    pop_info = pd.read_csv(os.path.join(base_path, 'popularity.csv'))
    stat_info = pd.read_csv(os.path.join(base_path, 'stat.csv'))
    symbol = pd.read_csv(os.path.join(base_path, 'symbol_info.csv'))

    # char_info preprocessing
    char_info = char_info.drop([
    'date','character_name','character_gender','character_class_level',
    'character_guild_name','character_image','access_flag','character_exp',
    'liberation_quest_clear_flag','liberation_quest_clear'
    ], axis=1)

    # dojang preprocessing
    dojang = dojang.drop([
        'date','character_class','world_name','date_dojang_record'
        ], axis=1)

    # pop_info preprocessing
    pop_info = pop_info.drop('date', axis=1)


    # stat preprocessing

    stat_info['final_stat'] = stat_info['final_stat'].apply(ast.literal_eval)

    df_stat = pd.DataFrame([
        {d['stat_name'] : d['stat_value'] for d in stat_list}
        for stat_list in stat_info['final_stat']
    ])

    df_stat['nickname'] = stat_info['nickname'].values

    cols = df_stat.columns.tolist()

    cols = ['nickname'] + [col for col in cols if col != 'nickname']

    df_stat = df_stat[cols]

    # symbol perprocessing
    symbol['symbol'] = symbol['symbol'].apply(ast.literal_eval)

    df_symbol = pd.DataFrame([
        {d['symbol_name'] : d['symbol_force'] for d in symbol_list}
        for symbol_list in symbol['symbol']
    ])

    df_symbol['nickname'] = symbol['nickname'].values

    cols = df_symbol.columns.tolist()

    df_symbol = df_symbol[cols]

    # symbol 은 정보가 너무 많고 str이 많아서 symbol_force만을 feature engineering을 통해 새로운 DataFrame 만듦
    symbol_cols = df_symbol.columns.drop('nickname')

    df_symbol['force_sum'] = df_symbol[symbol_cols].fillna(0).astype(float).sum(axis=1)
    df_symbol['force_mean'] = df_symbol[symbol_cols].fillna(0).astype(float).mean(axis=1)
    df_symbol['force_min'] = df_symbol[symbol_cols].fillna(0).astype(float).min(axis=1)

    symbol_select_cols = ['nickname','force_sum','force_mean','force_min']

    df_symbol = df_symbol[symbol_select_cols]

    return char_info, dojang, pop_info, df_stat, df_symbol


# 위에 원하는 형태로 각 데이터들이 전처리 됨
# key값은 nickname을 통해서 하나의 데이터로 병합

def merge_data(char_info, dojang, pop_info, df_stat, df_symbol):
    # nickname 기준으로 병합
    df = char_info.merge(dojang, on='nickname', how='inner')
    df = df.merge(pop_info, on='nickname', how='inner')
    df = df.merge(df_stat, on='nickname', how='inner')
    df = df.merge(df_symbol, on='nickname', how='inner')

    # key값인 nickname을 제일 앞에
    cols = df.columns.tolist()
    cols = ['nickname'] + [col for col in cols if col != 'nickname']
    df = df[cols]

    return df

# merge data 저장
def save_data(df, save_path='./dojang_analysis/data/merge_data.csv'):
    df.to_csv(save_path, index=False, encoding='utf-8-sig')

def main():
    char_info, dojang, pop_info, df_stat, df_symbol = data_processing()
    df = merge_data(char_info, dojang, pop_info, df_stat, df_symbol) 
    save_data(df)

if __name__ == '__main__':
    main()
