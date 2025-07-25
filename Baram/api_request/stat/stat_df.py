# stat.csv의 컬럼 stat을 풀어쓰기 위한 스크립트

import pandas as pd
import ast
import os

def stat_column(stat_str):
    try:
        stat_list = ast.literal_eval(stat_str)
        return {item['stat_name'] : int(item['stat_value']) for item in stat_list}
    except (ValueError, SyntaxError):
        return {}
    
def main():
    input_path = './Baram/data/stat.csv'
    output_path = './Baram/data/stat_df.csv'

    df = pd.read_csv(input_path)

    # stat column parsing
    stat_parsed = df['stat'].apply(stat_column)
    stat_expanded = pd.json_normalize(stat_parsed)

    # merge
    # stat의 딕셔너리 형태의 컬럼 제거 -> 컬럼 확장
    stat_df = pd.concat([df.drop(columns=['stat']), stat_expanded], axis=1)

    # save
    stat_df.to_csv(output_path, index=False, encoding='utf-8-sig')

if __name__ == '__main__':
    main()