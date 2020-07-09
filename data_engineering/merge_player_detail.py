import pandas as pd


total = []
col =[]
for i in range(2009,2020):
    #新增season欄位
    df = pd.read_csv('./player_data/pitcher_id_%s.csv'%i)
    sea = []
    for j in range(len(df)):
        sea.append(i)
    df['season'] = pd.DataFrame(sea)
    print(df.head())
    for k in df.values.tolist():
        total.append(k)
    #取df columns製作新表格
    if i == 2019:
        for co in df:
            col.append(co)
new_df = pd.DataFrame(total,columns=col)
new_df.to_csv('./player_data/new_pitcher.csv',index=False)

df1 = pd.read_csv('./data/new_batter.csv')
df_batter = df1[['player_id','woba','season']]
print(df_batter)



#新增season欄位
season =[]
df_game = pd.read_csv('./games.csv')

for i in df_game.values.tolist():
    s = i[1][0:4]
    season.append(s)
df_game['season'] = pd.DataFrame(season)
df_game.to_csv('./data/games.csv',index= 0)

#
#合併表格球員資料
df_batter['woba'].astype(str)
df_batter.player_id = df_batter.player_id.astype(str)
df_batter.season = df_batter.season.astype(str)
df_batter.woba = df_batter.woba.astype(str)

for i in range(1,10):
    df_game = pd.read_csv('./data/games.csv')
    df_game["away_%s" % i] = df_game["away_%s" % i].astype(str)
    df_game["home_%s" % i] = df_game["home_%s" % i].astype(str)
    df_game.season = df_game.season.astype(str)
    df_game = pd.merge(df_game, df_batter, left_on=["away_%s"%i,'season'], right_on=['player_id','season'],how='left').drop("away_%s"%i,axis=1)
    df_game = pd.merge(df_game, df_batter, left_on=["home_%s" % i, 'season'], right_on=['player_id', 'season'],how='left').drop("home_%s" % i, axis=1)
    df_game.to_csv('./data/games.csv',index= 0)
    print(df_game)

