# match data를 제외한 나머지 basic, rank, recent, tier 데이터를 ouid 기준으로 병합
# match data를 제외하는 이유는 match data는 match_id 를 기준으로 데이터가 구성 되어있음
# 즉, ouid를 기준으로 구성되어있는 데이터들과는 다른 구조임
# 따라서 match data를 제외한 나머지 4개의 데이터 병합

import pandas as pd
import os

df_basic = pd.read_csv('./SA/analysis/final_data/basic_final.csv')
df_match = pd.read_csv('./SA/analysis/final_data/df_match_quik_clan.csv')
df_rank = pd.read_csv('./SA/analysis/final_data/rank_final.csv')
df_recent = pd.read_csv('./SA/analysis/final_data/recent_final.csv')
df_tier = pd.read_csv('./SA/analysis/final_data/tier_final.csv')

# 1. rank + recent
df_merged = pd.merge(df_rank, df_recent, on='ouid', how='inner')

# 2. + tier
df_merged = pd.merge(df_merged, df_tier, on='ouid', how='inner')

# 3. + basic
df_merged = pd.merge(df_merged, df_basic, on='ouid', how='inner')

# 4. Unnamed: 0 제거
df_merged = df_merged.drop(['Unnamed: 0'], axis=1)


# 컬럼 순서 재배치
cols = df_merged.columns.tolist()
cols.remove('ouid')
cols = ['ouid'] + cols  # ouid를 맨 앞에 배치 (key값이므로 그게 난 편함)
df_merged = df_merged[cols]
df_merged = df_merged.dropna() # 결측값이 19개 존재함 최근 활동이 없는 유저인것으로 확인됨


### match data 필터링
## 현재 match data 는 'match_type'이 '퀵매치 클랜전' 하나의 값으로만 구성되어 있음 따라서 해당 컬럼 제거
## 'match_mode'또한 전부 '폭파미션'으로 구성되어 있으므로 해당 컬럼 제거

df_match = df_match.drop(['match_type','match_mode'], axis=1)

# 데이터 저장
df_match.to_csv('./SA/analysis/df_match.csv', index=False, encoding='utf-8-sig')
df_merged.to_csv('./SA/analysis/df_merged.csv', index=False, encoding='utf-8-sig')