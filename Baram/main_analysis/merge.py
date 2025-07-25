# basic.csv 에 key값인 ocid를 빼버림..ㅠ 여기서 병합해서 넣어야함
# API를 다시 호출하기엔 호출량이 늘어나므로 여기서 데이터 병합 후 진행
# key값은 character_name과 server_name으로 해야함

import pandas as pd

ocid = pd.read_csv('./Baram/data/ocid.csv')
basic = pd.read_csv('./Baram/data/basic.csv')
stat = pd.read_csv('./Baram/data/stat_df.csv')

# 중복 제거
ocid_keys = ocid[['character_name', 'server_name', 'ocid']].drop_duplicates(subset=['character_name', 'server_name'])
basic = basic.drop_duplicates(subset=['character_name', 'server_name'])

# 병합
basic_with_ocid = basic.merge(ocid_keys, on=['character_name', 'server_name'], how='inner')

# stat 쪽 정리
stat_trimmed = stat.drop(columns=['character_name', 'server_name', 'job'], errors='ignore')

df_merged = basic_with_ocid.merge(stat_trimmed, on='ocid', how='inner')

# 중복된 데이터가 있어서 제거
df_merged = df_merged.drop_duplicates()

# 저장
output_path = './Baram/main_analysis/data/merged_df.csv'
df_merged.to_csv(output_path, index=False, encoding='utf-8-sig')