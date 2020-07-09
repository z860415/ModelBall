import MySQLdb
import pandas as pd
import time

# db = MySQLdb.connect(host='1.tcp.jp.ngrok.io',user='balao1312'\
#                      ,passwd='clubgogo',db='MoneyBallDatabase', port=23879, charset='utf8')
#
# cursor = db.cursor() #建立游標
#
# sql_str='select * from game_odds'
# cursor.execute(sql_str)
# df = pd.DataFrame(cursor.fetchall())
# df.to_csv('odds.csv', encoding='utf8', index=False)
# db.close()
#
# df.head()

# game = pd.read_csv('demo.csv')
# odds = pd.read_csv('odds.csv')
#
# print(game.head() ,'\n')
# print(odds.head())

#將machup主客隊分成各別columns主隊/客隊
# game_home = []
# game_away = []
# for i in game['machup'].values:
#     game_home.append(i.split('@')[1])
# for j in game['machup'].values:
#     game_away.append(j.split('@')[0])
# home = pd.DataFrame(game_home)
# away = pd.DataFrame(game_away)
# game['team_home'] = home
# game['team_away'] = away
# print(game.head())
# game.to_csv('demo.csv', encoding='utf8', index=False)
#batter2 = df_batter[df_batter['player'].isin([b]) & df_batter['season'].isin([str(s)]) & df_batter['pitch_type'].isin([p])]


#轉換只取時間的小時以便後續篩選
# time1 = []
# time2 = []
# for i in game['time'].values:
#     time1.append(i[:2])
# for j in odds['time'].values:
#     time2.append(j[:2])
# game['time'] = pd.DataFrame(time1)
# odds['time'] = pd.DataFrame(time2)
# game.to_csv('demo.csv', encoding='utf8', index=False)
# odds.to_csv('odds.csv', encoding='utf8', index=False)


# mix_table = []
# for i in game.values:
#     #print(i[0:4])
#     odds_data1 = odds[odds.day.isin([i[0]]) & odds.home.isin([i[2]]) & odds.away.isin([i[3]])
#                       & odds['time'] >= i[1]-2 & odds['time'] <= i[1]+2 ]
#     print(type(odds[odds['time']]))
#     print(type(i[1]))
    #print(type(odds_data1.time))
    #print(odds_data1['time'].values[0])



#     if odds_data1['time'] -2 <= i[1] and odds_data1['time'] >= i[1]:
#         odds_data2 = odds_data1
#     else:
#         pass
#
#     a = [i.values,odds_data2['total'],odds_data2['over'],odds_data2['under']]
#     mix_table.append(a)
# print(mix_table).

# df=game.merge(odds,left_on=['date','time','team_home','team_away'],right_on=['day','time','home','away'],how='left')
# df.to_csv('test.csv', encoding='utf8', index=False)

df = pd.read_csv('testtttttttt.csv')#.values.tolist()
# df.dropna(axis=0, how='any', inplace=True)
# df.to_csv('test.csv', encoding='utf8', index=False)
# print(df)
# df.drop_duplicates(keep='first', inplace=True)
# print(df)
# df.to_csv('test.csv', encoding='utf8', index=False)
# total_s = []
# for i in range(df.shape[0]) :
#     #print(df.iat[i,24],df.iat[i,25])
#     a = df.iat[i,24]
#     b = df.iat[i,25]
#     total_s.append(float(a)+float(b))
# df['total_score'] = pd.DataFrame(total_s)


result = []
for j in range(df.shape[0]) :
    print(j)
    odds_t = float(df.iat[j,47])
    game_t = float(df.iat[j,46])
    #print(odds_t)
    #print(game_t)
    if game_t > odds_t:
        result.append(1)
    elif game_t <= odds_t:
        result.append(0)

df['result'] = pd.DataFrame(result)
print(result)
df.to_csv('test.csv', encoding='utf8', index=False)
