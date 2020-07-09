import pandas as pd

df = pd.read_csv('./total_data.csv')
a = pd.to_datetime(df['date'] + ' ' + df['time'])
timediff = pd.Timedelta('4 hours 0 minutes 0 seconds')
b = a-timediff
new_date = []
new_time = []
for i in b.dt.strftime('%Y-%m-%d'):
    new_date.append(i)
for j in b.dt.strftime('%H:%M'):
    new_time.append(j)
data2 = pd.DataFrame({'date':new_date , 'time':new_time})
df[['date','time']] = data2[['date','time']]
df.to_csv("total_data.csv", encoding='utf_8_sig')
print(len(new_date))
print(len(new_time))
print(len(df['date']))
print(len(df['time']))
print(len(df))