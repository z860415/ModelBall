import pandas as pd
import numpy as np
import MySQLdb

#從 mysql 讀 id_reference 的 table
# db = MySQLdb.connect(host='1.tcp.jp.ngrok.io',user='balao1312'\
#                      ,passwd='clubgogo',db='MoneyBallDatabase', port=23879, charset='utf8')
#
# cursor = db.cursor() #建立游標
#
# sql_str='select * from statcast'
# cursor.execute(sql_str)
# df = pd.DataFrame(cursor.fetchall())
# df.to_csv('statcast.csv', encoding='utf8', index=False)
# db.close()

#從sql儲存statcast表個至本地，並命名為statcast2開啟
df = pd.read_csv('statcast2.csv')

print(df['pitch_name'].unique())#檢視pitch_name內所有種類
print(df.columns)

df2 = df[df.season > 2009]#statcast表格包含2008-2019所有資料，將2010以前資料刪除
df2.to_csv('statcast2.csv', encoding='utf8', index=False)
print(df.head())
print(df['des'].unique())#確認個欄位不重複值
print(df['events'].unique())




#定義function將各別球種分類，重新命名
def pitch_rename(s):
    if s == '4-Seam Fastball' or s == '2-Seam Fastball' or s == 'Fastball' or s == 'Sinker' or s == 'Screwball':
        return 'FB'
    if s == 'Slider':
        return 'SL'
    if s == 'Cutter':
        return 'CT'
    if s == 'Knuckle Curve' or s == 'Curveball':
        return 'CB'
    if s == 'Changeup':
        return 'CH'
    if s == 'Split Finger' or s == 'Forkball':
        return 'SF'
    if s == 'Knuckle Ball':
        return 'KN'
    else:
        return ''




#套用rename function將pitch_name欄位值重新命名(為了與pitcher表格一致)
new = []
for i in df['pitch_name'].values:
    a = pitch_rename(i)
    new.append(a)
x = pd.DataFrame(new)
print(df['pitch_name'])

df['pitch_name'] = x
df.drop('pitch_type',axis=1,inplace=True)
print(df.head())
df.to_csv('statcast2.csv', encoding='utf8', index=False)





#groupby方式將賽季、球員、球種分類
df = pd.read_csv('statcast2.csv')
data = []
grouped = df.groupby(['season','batter','pitch_name'])

for name,group in grouped:
    print (name)
    print(group)
    season = name[0]  #name為分類後的season,batter,pitch_name
    player = name[1]  #group為分類後的各分類表格
    pitch_type = name[2]
    total_times = group['pitch_name'].value_counts()[0] #計算球員遇到該球種共幾次
    try:
        swin_time = group.des.isin(['hit_into_play' , 'hit_into_play_no_out' , 'foul' , 'foul_tip' , 'swinging_strike' , 'hit_into_play_score' , 'swinging_strike_blocked']).value_counts()[1]  #計算特定字串總出現次數，isin()回傳為布林值，用value_counts計算true/false次數
    except:
        swin_time = 0
    try:
        single = group.events.isin(['single']).value_counts()[1]
    except:
        single = 0
    try:
        double = group.events.isin(['double']).value_counts()[1]
    except:
        double = 0
    try:
        triple = group.events.isin(['triple']).value_counts()[1]
    except:
        triple = 0
    try:
        home_run = group.events.isin(['home_run']).value_counts()[1]
    except:
        home_run = 0

    data.append([season,player,pitch_type,total_times,swin_time,single,double,triple,home_run])

new_data = pd.DataFrame(data,columns=['season','player','pitch_type','total_times','swin_time','single','double','triple','home_run']) #計算完成後產生新表格並儲存
#new_data.to_csv('ttt.csv', encoding='utf8', index=False)





# #新增score欄位計算打擊成績
df = pd.read_csv('ttt.csv')
print(df.head())
score = (0.89 * df.single + 1.27 * df.double + 1.62 * df.triple + 2.1 * df.home_run) / df.swin_time
df['score']=score
print(df.head())

df.to_csv('ttt.csv', encoding='utf8', index=False)






#score空值填補中位數
df = pd.read_csv('ttt.csv',na_values='')

q_50 = np.percentile(df[~df['score'].isnull()]['score'], 50)
df.loc[df['score'].isnull(),'score'] = q_50
print(q_50)
print(df)
df.to_csv('ttt.csv', encoding='utf8', index=False)



