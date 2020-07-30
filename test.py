import web_crawler
import pandas as pd
from work.DE import DE



game = pd.read_csv('./game2020-07-29.csv')
df = DE(game)
print(df)
print('=====================================')
from work.prediction import modle_train
modle_train()
df_set = pd.read_csv('./pre_test.csv',na_values='')
df_set.drop_duplicates(subset=['date', 'team_home', 'team_away'], keep='last', inplace=True)
df_set.dropna(axis=0, how='any', inplace=True)
df_set.to_csv('./pre_test.csv', index=False)
print(df_set)
print('finish')