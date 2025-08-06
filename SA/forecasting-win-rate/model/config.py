rf_params = {
    'n_estimators': [100, 150, 200, 250, 300],
    'max_depth': [None, 5, 10, 15, 20],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2],
    'max_features': ['sqrt', 'log2']
}

xgb_params = {
    'n_estimators': [100, 150, 200, 250],
    'max_depth': [3, 5, 7, 10],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

lgbm_params = {
    'n_estimators': [100, 150, 200, 250, 300],
    'max_depth': [-1, 5, 10, 15],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'num_leaves': [31, 50, 70],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

importance_features = [
    'total_matches', 'grade_ranking', 'season_grade_ranking',
    'recent_win_rate', 'recent_kill_death_rate', 'recent_assault_rate',
    'recent_sniper_rate', 'recent_special_rate',
    'solo_rank_match_score', 'party_rank_match_score'
]
