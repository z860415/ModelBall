import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
import matplotlib.pyplot as plt
from sklearn import preprocessing
import datetime

df = pd.read_csv('./demo_games.csv',na_values='')
print(df)



print('=====時間特徵分解=====')
df['pickup_datetime'] = df['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y/%m/%d'))
df.drop(['date'],axis=1,inplace=True)
df['pickup_woy'] = df['pickup_datetime'].apply(lambda x: datetime.datetime.strftime(x, '%W')).astype('int64')
df.drop(['pickup_datetime'],axis=1,inplace=True)
print(df.head())



print('=====主隊進行one_hot_encoding=====')
df = df.join(pd.get_dummies(df.home))
df.drop(['home','away','home_total_x','away_total_x','game_total','time_x','over','under'],axis=1,inplace=True)
print(df)



print('=====選取int64/folat64數值型欄位=====')
num_features = []
for dtype, feature in zip(df.dtypes, df.columns):
    if dtype == 'float64' or dtype == 'int64':
        num_features.append(feature)
print(f'{len(num_features)} 個數值型欄位 : {num_features}\n')



print('=====再把只有 2 值 (通常是 0,1) 的欄位去掉=====')
numeric_columns = list(df[num_features].columns[list(df[num_features].apply(lambda x:len(x.unique())!=2 ))])
print("Numbers of remain columns: %i" % len(numeric_columns))



print('=====選取正規化欄位=====')
'''
Z-Score
利用原始資料的均值（mean）和標準差（standard deviation）進行資料的標準化，
適用於資料的最大值和最小值未知的情況，或有超出取值範圍的離群資料的情況。
**公式：**新資料=（原始資料-均值）/標準差
'''
# zscore = preprocessing.StandardScaler()
# df[numeric_columns] = zscore.fit_transform(df[numeric_columns])
'''
RobustScaler
有時候，資料集中存在離群點，就需要利用RobustScaler針對離群點做標準化處理，
該方法對資料中心化的資料的縮放更強的引數控制能力。
'''
# robust = preprocessing.RobustScaler()
# df[numeric_columns] = robust.fit_transform(df[numeric_columns])
'''MaxAbs
最大值絕對值標準化(MaxAbs)，根據最大值的絕對值進行標準化
公式：新資料 = 原始資料 / |原始資料的最大值|
其中max為x鎖在列的最大值，資料區間為[-1, 1]，因此適用於稀疏矩陣。
'''
maxabs = preprocessing.MaxAbsScaler()
df[numeric_columns] = maxabs.fit_transform(df[numeric_columns])



print('=====將result欄位做LabelEncoder=====')
le = LabelEncoder()
df['result'] = le.fit_transform(df['result'])




print('=====離群值處理=====')
for i in numeric_columns:
    Q01 = np.percentile(df[i], 1)
    Q99 = np.percentile(df[i], 99)
    # 替换异常值为指定的分位数
    if Q01 > df[i].min():
        df[i].loc[df[i] < Q01] = Q01
    if Q99 < df[i].max():
        df[i].loc[df[i] > Q99] = Q99



# print('=====顯示欄位與目標值的散佈圖=====')
# import seaborn as sns
# import matplotlib.pyplot as plt
# train_Y = df['result']
# train_num = train_Y.shape[0]
# for i in numeric_columns:
#     sns.distplot(df[i][:train_num])
#     plt.show()



print('=====切分訓練集/測試集=====')
train_x = df.drop(['result'],axis=1)
train_y = df['result']
x_train, x_test, y_train, y_test = train_test_split(train_x, train_y, test_size=0.3, random_state=4)

print('=====建立一個羅吉斯回歸模型=====')

regr = LogisticRegression()
regr.fit(x_train, y_train)
y_pred = regr.predict(x_test)
acc = accuracy_score(y_test, y_pred)
print("羅吉斯回歸預測結果: ", acc)



correlations = abs(df.corr()['result'].sort_values())
print('Most Positive Correlations:\n', abs(correlations).sort_values())

print('=====篩選相關係數大於 0.01 或小於 0.01 的特徵=====')
high_list = list(df.columns[abs(correlations >= 0.01)])
high_list.remove('result')
#high_list.pop(-1)
print(high_list)



print('=====0.01特徵 + 邏輯斯迴歸=====')
train_X = df[high_list]
x_train, x_test, y_train, y_test = train_test_split(train_X, train_y, test_size=0.3, random_state=4)
regr = LogisticRegression()
regr.fit(x_train, y_train)
y_pred = regr.predict(x_test)
acc = accuracy_score(y_test, y_pred)
print("0.01特徵 + 邏輯斯迴歸: ", acc)



# print('=====SVM=====')
# from sklearn import svm
# from sklearn.model_selection import train_test_split
# #from https://pyecontech.com/2020/04/11/python%E5%AF%A6%E4%BD%9C-%E6%94%AF%E6%8F%B4%E5%90%91%E9%87%8F%E6%A9%9F-svm/
# train_x = df[high_list]
# x_train, x_test, y_train, y_test = train_test_split(train_x, train_y, test_size=0.3, random_state=4)
# clf=svm.SVC(kernel='linear',C=23,gamma='auto')
# clf.fit(x_train,y_train)
# y_test_predict = clf.predict(x_test)
# #準確度分析
# print(clf.score(x_train,y_train))
# print(clf.score(x_test, y_test))
# #精確度
# from sklearn.metrics import accuracy_score
# Ypred = clf.predict(x_test)
# print("SVM_accuracy_score",accuracy_score(y_test, Ypred),'\n','\n')
#
# #完整模型評估報告
# from sklearn.metrics import classification_report
# print(classification_report(y_test, Ypred))
#
#
#
# # print('=====隨機森林=====')
# # from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
# # from sklearn.model_selection import train_test_split
# # from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
# # # 切分訓練集/測試集
# # train_x = df[high_list]
# # x_train, x_test, y_train, y_test = train_test_split(train_x, train_y, test_size=0.3, random_state=4)
# # # 建立一個羅吉斯回歸模型
# # regr = RandomForestClassifier()
# # # 將訓練資料丟進去模型訓練
# # regr.fit(x_train, y_train)
# # # 將測試資料丟進模型得到預測結果
# # y_pred = regr.predict(x_test)
# # acc = accuracy_score(y_test, y_pred)
# # print("RandomForestClassifier Accuracy: ", acc)
#
#
#
# print('=====SVM模型儲存=====')
# import joblib
#
# joblib.dump(clf,'Money_ball.pkl')


print('=====SVM模型預測=====')
import joblib
clf2 = joblib.load('Money_ball.pkl')
train_x = df[high_list]
df['prediction'] = pd.DataFrame(clf2.predict(train_x))
df.to_csv('./prediction.csv',index= 0)
