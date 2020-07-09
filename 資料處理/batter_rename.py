import pandas as pd

years = input('請輸入年份：')
month_start = int(input('請輸入開始月份：'))
month_end = int(input('請輸入結束月份：'))+1
columns = ['season','Name','Age','#days','Lev','Tm','G','PA','AB','R','H','2B','3B','HR','RBI','BB','IBB','SO','HBP','SH','SF','GDP','SB','CS','BA','OBP','SLG','OPS']
for month in range(month_start,month_end):
    if len(str(month)) < 2 :
        month = '0'+str(month)
    file = pd.read_csv('{}-{}_batting.csv'.format(years,month),index_col=0).reset_index(drop=True)
    #新增年份欄位
    year = []
    for i in range(0,len(file)):
        year.append(years)
    file['season'] = year
    file.to_csv('{}-{}_batting.csv'.format(years,month), encoding='utf_8_sig',columns=columns)
