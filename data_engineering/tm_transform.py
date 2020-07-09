import pandas as pd


def team_rename(name):
    if name == "Dodgers":
        return "LAD"
    if name == "Red Sox":
        return "BOS"
    if name == "Brewers":
        return "MIL"
    if name == "Astros":
        return "HOU"
    if name == "Yankees":
        return "NYY"
    if name == "Braves":
        return "ATL"
    if name == "Indians":
        return "CLE"
    if name == "Rockies":
        return "COL"
    if name == "Cubs":
        return "CHC"
    if name == "Royals":
        return "KC"
    if name == "Mariners":
        return "SEA"
    if name == "Padres":
        return "SD"
    if name == "Mets":
        return "NYM"
    if name == "Twins":
        return "MIN"
    if name == "Reds":
        return "CIN"
    if name == "Angels":
        return "LAA"
    if name == "Giants":
        return "SF"
    if name == "Phillies":
        return "PHI"
    if name == "Orioles":
        return "BAL"
    if name == "Diamondbacks":
        return "ARI"
    if name == "White Sox":
        return "CWS"
    if name == "Cardinals" or name == "St.Louis Cardinals":
        return "STL"
    if name == "Blue Jays":
        return "TOR"
    if name == "Nationals":
        return "WSH"
    if name == "Athletics":
        return "OAK"
    if name == "Rangers":
        return "TEX"
    if name == "Pirates":
        return "PIT"
    if name == "Marlins" or name == "Florida Marlins":
        return "MIA"
    if name == "Tigers":
        return "DET"
    if name == "Rays":
        return "TB"
    else:
        print("No name match found for "+name)
        return ""

# if __name__ == '__main__':
#     new_home = []
#     df = pd.read_csv('pitcher_data.csv')
#     for i in df['Team']:
#         b = team_rename(i)
#         new_home.append(b)
#     df['Team'] = pd.DataFrame(new_home)
#     print(df)
#     df.to_csv('pitcher_data.csv',index=False)

# df = pd.read_csv('games.csv')
# df2 = pd.read_csv('id_map.csv')
# print(df2)
# print(df)
#
# df.playerid = df.playerid.astype(str)
# df2.IDFANGRAPHS = df2.IDFANGRAPHS.astype(str)
# df2.MLBID = df2.MLBID.astype(str)
#
# df3 = pd.merge(df, df2, left_on=['playerid'], right_on=['IDFANGRAPHS'],how='left')
# df3.to_csv('batter_data.csv',index=False)

# print(df)
# away = []
# home = []
# for i in df['matchup']:
#     a = i.split('@')[0]
#     away.append(a)
#     b = i.split('@')[1]
#     home.append(b)
# df['home'] = pd.DataFrame(home)
# df['away'] = pd.DataFrame(away)
#
# print(df)
# df.to_csv('games.csv',index=False)
# df2 = pd.read_csv('demo.csv')
# print(df2)
# df3 = pd.merge(df, df2, left_on=['date','home','away','umpire_K/BB'], right_on=['date','team_home','team_away','umpire_K/BB'],how='left')
#
# print(df3)
# #df3.to_csv('demo_games.csv',index=False)
#
# df3.drop_duplicates( subset=None,keep='first', inplace=True)
# df3.to_csv('demo_games.csv',index=False)


df = pd.read_csv('demo_games.csv',dtype={'home_pitcher':str,'season':str})
df2 = pd.read_csv('./player_data/pitcher_data.csv',dtype={'ID':str,'Season':str})


# season=[]
# for sea in df['date']:
#     season.append(sea[0:4])
# df['season'] = pd.DataFrame(season)
# df.to_csv('demo_games.csv')
print(df.columns)
print('\n',df2.columns)
#
#


# df.home_pitcher = df.home_pitcher.astype(str)
# df.season = df.season.astype(str)
# df2.Season = df2.Season.astype(str)
# df2.ID = df2.ID.map(lambda x : ('%.0f')%x ).astype(str)

print(df.home_pitcher)
print(df.season)
print(df2.Season)
print(df2.ID)
print(df2)
#
# new = []
# for i in df2.ID:
#     new.append(i[0:6])
# df2.ID = pd.DataFrame(new).astype(int)
# df2.to_csv('./player_data/pitcher_data.csv',index=False)
# print(df2.ID)
#
#
df3 = pd.merge(df, df2, left_on=['season','home_pitcher'], right_on=['Season','ID'],how='left')

print(df3)
df3.to_csv('./testttttt.csv',index=False)
