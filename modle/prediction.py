import pandas as pd
import matplotlib.pyplot as plt


print('=====row_data_分年份儲存=====')
# for i in range (2010,2020):
#     df= pd.read_csv('./money_line.csv')
#     a = df[df.season == i]
#     a.to_csv('money_line_%s.csv'%i,index=False)


print('=====試算各年分現金流=====')
for i in range (2010,2020):
    df2 = pd.read_csv('money_line_%s.csv' % i)
    money = 1
    money2 = 1
    money_line_Kelly = []
    money_line = []
    for res, pre in zip(df2['result'], df2['prediction']):
        if res == pre:
            money = money +  (money * 0.12 * 0.9)
        if res != pre:
            money = money -  (money * 0.12)
        money_line_Kelly.append(money)
    for res, pre in zip(df2['result'], df2['prediction']):
        if res == pre:
            money2 = money2 +  0.09
        if res != pre:
            money2 = money2 -  0.1
        money_line.append(money2)
    df2['money_line_Kelly'] = pd.DataFrame(money_line_Kelly)
    df2['money_line'] = pd.DataFrame(money_line)
    y = df2.money_line.values.tolist()
    x = df2.date.values.tolist()
    df2['date'] = pd.to_datetime(df2['date'])
    ax1 = df2.plot(x='date', y=['money_line','money_line_Kelly'],title='season_%s'%i,linewidth = 1)
    plt.xlabel('date')
    plt.ylabel('money_line')
    plt.show()
    df2.to_csv('money_line_%s.csv'%i, index=0)


