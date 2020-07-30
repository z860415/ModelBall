import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn import preprocessing
import datetime


def modle_train():

    total = pd.read_csv('./finall_data2.csv', na_values='')
    df2 = pd.read_csv('./finall_data.csv', na_values='')
    df2['date'] = df2['date'].apply(lambda x:x.replace('-','/'))
    df2.drop(['time'],axis=1 ,inplace=True)
    df2.drop('umpire_K/BB', axis=1, inplace=True)
    total.drop('umpire_K/BB', axis=1, inplace=True)
    new = []


    for data in range (0,len(df2)):
        df = total.append(df2.iloc[data],ignore_index=True)
        print(df)
        # 空值填補中位數
        na_fill = ['a_v_1', 'a_v_2', 'a_v_3', 'a_v_4', 'a_v_5', 'a_v_6', 'a_v_7', 'a_v_8', 'a_v_9',
                   'h_v_1', 'h_v_2', 'h_v_3', 'h_v_4', 'h_v_5', 'h_v_6', 'h_v_7', 'h_v_8', 'h_v_9']
        # df = pd.read_csv('./demo_v4.csv',na_values='0')
        for i in na_fill:
            q_50 = np.percentile(df[~df[i].isnull()][i], 50)
            df.loc[df[i].isnull(), i] = q_50
        na_fill = ['K/9_x', 'BB/9_x', 'K/BB_x', 'HR/9_x', 'K%_x', 'BB%_x', 'AVG_x', 'WHIP_x', 'BABIP_x', 'LOB%_x',
                   'ERA-_x', 'FIP-_x', 'xFIP-_x', 'ERA_x', 'FIP_x', 'E-F_x', 'xFIP_x', 'SIERA_x', 'K/9_y', 'BB/9_y',
                   'K/BB_y',
                   'HR/9_y', 'K%_y', 'BB%_y', 'AVG_y', 'WHIP_y', 'BABIP_y', 'LOB%_y', 'ERA-_y', 'FIP-_y', 'xFIP-_y',
                   'ERA_y', 'FIP_y', 'E-F_y', 'xFIP_y', 'SIERA_y', 'BB%_x.1', 'K%_x.1', 'ISO_x', 'BABIP_x.1', 'AVG_x.1',
                   'OBP_x',
                   'SLG_x', 'wOBA_x', 'wRC+_x', 'BsR_x', 'Off_x', 'Def_x', 'WAR_x', 'BB%_y.1', 'K%_y.1', 'ISO_y',
                   'BABIP_y.1',
                   'AVG_y.1', 'OBP_y', 'SLG_y', 'wOBA_y', 'wRC+_y', 'BsR_y', 'Off_y', 'Def_y', 'WAR_y', 'BB%_x.2',
                   'K%_x.2',
                   'ISO_x.1', 'BABIP_x.2', 'AVG_x.2', 'OBP_x.1', 'SLG_x.1', 'wOBA_x.1', 'wRC+_x.1', 'BsR_x.1',
                   'Off_x.1',
                   'Def_x.1', 'WAR_x.1', 'BB%_y.2', 'K%_y.2', 'ISO_y.1', 'BABIP_y.2', 'AVG_y.2', 'OBP_y.1', 'SLG_y.1',
                   'wOBA_y.1', 'wRC+_y.1', 'BsR_y.1', 'Off_y.1', 'Def_y.1', 'WAR_y.1', 'BB%_x.3', 'K%_x.3', 'ISO_x.2',
                   'BABIP_x.3', 'AVG_x.3', 'OBP_x.2', 'SLG_x.2', 'wOBA_x.2', 'wRC+_x.2', 'BsR_x.2', 'Off_x.2',
                   'Def_x.2',
                   'WAR_x.2', 'BB%_y.3', 'K%_y.3', 'ISO_y.2', 'BABIP_y.3', 'AVG_y.3', 'OBP_y.2', 'SLG_y.2', 'wOBA_y.2',
                   'wRC+_y.2', 'BsR_y.2', 'Off_y.2', 'Def_y.2', 'WAR_y.2', 'BB%_x.4', 'K%_x.4', 'ISO_x.3', 'BABIP_x.4',
                   'AVG_x.4', 'OBP_x.3', 'SLG_x.3', 'wOBA_x.3', 'wRC+_x.3', 'BsR_x.3', 'Off_x.3', 'Def_x.3', 'WAR_x.3',
                   'BB%_y.4', 'K%_y.4', 'ISO_y.3', 'BABIP_y.4', 'AVG_y.4', 'OBP_y.3', 'SLG_y.3', 'wOBA_y.3', 'wRC+_y.3',
                   'BsR_y.3', 'Off_y.3', 'Def_y.3', 'WAR_y.3', 'BB%_x.5', 'K%_x.5', 'ISO_x.4', 'BABIP_x.5', 'AVG_x.5',
                   'OBP_x.4', 'SLG_x.4', 'wOBA_x.4', 'wRC+_x.4', 'BsR_x.4', 'Off_x.4', 'Def_x.4', 'WAR_x.4', 'BB%_y.5',
                   'K%_y.5', 'ISO_y.4', 'BABIP_y.5', 'AVG_y.5', 'OBP_y.4', 'SLG_y.4', 'wOBA_y.4', 'wRC+_y.4', 'BsR_y.4',
                   'Off_y.4', 'Def_y.4', 'WAR_y.4', 'BB%_x.6', 'K%_x.6', 'ISO_x.5', 'BABIP_x.6', 'AVG_x.6', 'OBP_x.5',
                   'SLG_x.5', 'wOBA_x.5', 'wRC+_x.5', 'BsR_x.5', 'Off_x.5', 'Def_x.5', 'WAR_x.5', 'BB%_y.6', 'K%_y.6',
                   'ISO_y.5', 'BABIP_y.6', 'AVG_y.6', 'OBP_y.5', 'SLG_y.5', 'wOBA_y.5', 'wRC+_y.5', 'BsR_y.5',
                   'Off_y.5',
                   'Def_y.5', 'WAR_y.5', 'BB%_x.7', 'K%_x.7', 'ISO_x.6', 'BABIP_x.7', 'AVG_x.7', 'OBP_x.6', 'SLG_x.6',
                   'wOBA_x.6', 'wRC+_x.6', 'BsR_x.6', 'Off_x.6', 'Def_x.6', 'WAR_x.6', 'BB%_y.7', 'K%_y.7', 'ISO_y.6',
                   'BABIP_y.7', 'AVG_y.7', 'OBP_y.6', 'SLG_y.6', 'wOBA_y.6', 'wRC+_y.6', 'BsR_y.6', 'Off_y.6',
                   'Def_y.6',
                   'WAR_y.6', 'BB%_x.8', 'K%_x.8', 'ISO_x.7', 'BABIP_x.8', 'AVG_x.8', 'OBP_x.7', 'SLG_x.7', 'wOBA_x.7',
                   'wRC+_x.7', 'BsR_x.7', 'Off_x.7', 'Def_x.7', 'WAR_x.7', 'BB%_y.8', 'K%_y.8', 'ISO_y.7', 'BABIP_y.8',
                   'AVG_y.8', 'OBP_y.7', 'SLG_y.7', 'wOBA_y.7', 'wRC+_y.7', 'BsR_y.7', 'Off_y.7', 'Def_y.7', 'WAR_y.7',
                   'BB%_x.9', 'K%_x.9', 'ISO_x.8', 'BABIP_x.9', 'AVG_x.9', 'OBP_x.8', 'SLG_x.8', 'wOBA_x.8', 'wRC+_x.8',
                   'BsR_x.8', 'Off_x.8', 'Def_x.8', 'WAR_x.8', 'BB%_y.9', 'K%_y.9', 'ISO_y.8', 'BABIP_y.9', 'AVG_y.9',
                   'OBP_y.8', 'SLG_y.8', 'wOBA_y.8', 'wRC+_y.8', 'BsR_y.8', 'Off_y.8', 'Def_y.8', 'WAR_y.8', 'wOBA']

        for i in na_fill:
            try:
                q_50 = np.percentile(df[~df[i].isnull()][i], 50)
                df.loc[df[i].isnull(), i] = q_50
            except Exception as e:
                print(i)
                print(e)
                continue

        #print('=====時間特徵分解=====')
        df['pickup_datetime'] = df['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y/%m/%d'))
        df.drop(['date'],axis=1,inplace=True)
        df['pickup_woy'] = df['pickup_datetime'].apply(lambda x: datetime.datetime.strftime(x, '%W')).astype('int64')
        df.drop(['pickup_datetime'],axis=1,inplace=True)
        #print(df['pickup_woy'])




        #print('=====主隊進行one_hot_encoding=====')
        df = df.join(pd.get_dummies(df.team_home))
        df.drop(['team_home','team_away','over','under'],axis=1,inplace=True)
        #print(df)



        #print('=====選取int64/folat64數值型欄位=====')
        num_features = []
        for dtype, feature in zip(df.dtypes, df.columns):
            if dtype == 'float64' or dtype == 'int64':
                num_features.append(feature)
        #print(f'{len(num_features)} 個數值型欄位 : {num_features}\n')



        #print('=====再把只有 2 值 (通常是 0,1) 的欄位去掉=====')
        numeric_columns = list(df[num_features].columns[list(df[num_features].apply(lambda x:len(x.unique())!=2 ))])
        #print("Numbers of remain columns: %i" % len(numeric_columns))



        #print('=====選取正規化欄位=====')

        maxabs = preprocessing.MaxAbsScaler()
        df[numeric_columns] = maxabs.fit_transform(df[numeric_columns])





        #print('=====去除偏態(嘗試用Q01，Q99來代替離群值）=====')
        for i in numeric_columns:
            Q01 = np.percentile(df[i], 1)
            Q99 = np.percentile(df[i], 99)
            # 替換離群值至指定分位數
            if Q01 > df[i].min():
                df[i].loc[df[i] < Q01] = Q01
            if Q99 < df[i].max():
                df[i].loc[df[i] > Q99] = Q99





        #print('=====SVM模型預測=====')
        import joblib
        clf2 = joblib.load('./Money_ball_test.pkl')
        a = []
        col = ['a_v_1', 'a_v_2', 'a_v_3', 'a_v_4', 'a_v_5', 'a_v_6', 'a_v_7', 'a_v_8', 'a_v_9', 'h_v_1', 'h_v_2',
               'h_v_3', 'h_v_4', 'h_v_5', 'h_v_6', 'h_v_7', 'h_v_8', 'h_v_9', 'K/9_x', 'BB/9_x', 'K/BB_x', 'HR/9_x',
               'K%_x', 'BB%_x', 'AVG_x', 'WHIP_x', 'BABIP_x', 'LOB%_x', 'ERA-_x', 'FIP-_x', 'xFIP-_x', 'ERA_x', 'FIP_x',
               'E-F_x', 'xFIP_x', 'SIERA_x', 'K/9_y', 'BB/9_y', 'K/BB_y', 'HR/9_y', 'K%_y', 'BB%_y', 'AVG_y', 'WHIP_y',
               'BABIP_y', 'LOB%_y', 'ERA-_y', 'FIP-_y', 'xFIP-_y', 'ERA_y', 'FIP_y', 'E-F_y', 'xFIP_y', 'SIERA_y',
               'BB%_x.1', 'K%_x.1', 'ISO_x', 'BABIP_x.1', 'AVG_x.1', 'OBP_x', 'SLG_x', 'wOBA_x', 'wRC+_x', 'BsR_x',
               'Off_x', 'Def_x', 'WAR_x', 'BB%_y.1', 'K%_y.1', 'ISO_y', 'BABIP_y.1', 'AVG_y.1', 'OBP_y', 'SLG_y',
               'wOBA_y', 'wRC+_y', 'BsR_y', 'Off_y', 'Def_y', 'WAR_y', 'BB%_x.2', 'K%_x.2', 'ISO_x.1', 'BABIP_x.2',
               'AVG_x.2', 'OBP_x.1', 'SLG_x.1', 'wOBA_x.1', 'wRC+_x.1', 'BsR_x.1', 'Off_x.1', 'Def_x.1', 'WAR_x.1',
               'BB%_y.2', 'K%_y.2', 'ISO_y.1', 'BABIP_y.2', 'AVG_y.2', 'OBP_y.1', 'SLG_y.1', 'wOBA_y.1', 'wRC+_y.1',
               'BsR_y.1', 'Off_y.1', 'Def_y.1', 'WAR_y.1', 'BB%_x.3', 'K%_x.3', 'ISO_x.2', 'BABIP_x.3', 'AVG_x.3',
               'OBP_x.2', 'SLG_x.2', 'wOBA_x.2', 'wRC+_x.2', 'BsR_x.2', 'Off_x.2', 'Def_x.2', 'WAR_x.2', 'BB%_y.3',
               'K%_y.3', 'ISO_y.2', 'BABIP_y.3', 'AVG_y.3', 'OBP_y.2', 'SLG_y.2', 'wOBA_y.2', 'wRC+_y.2', 'BsR_y.2',
               'Off_y.2', 'Def_y.2', 'WAR_y.2', 'BB%_x.4', 'K%_x.4', 'ISO_x.3', 'BABIP_x.4', 'AVG_x.4', 'OBP_x.3',
               'SLG_x.3', 'wOBA_x.3', 'wRC+_x.3', 'BsR_x.3', 'Off_x.3', 'Def_x.3', 'WAR_x.3', 'BB%_y.4', 'K%_y.4',
               'ISO_y.3', 'BABIP_y.4', 'AVG_y.4', 'OBP_y.3', 'SLG_y.3', 'wOBA_y.3', 'wRC+_y.3', 'BsR_y.3', 'Off_y.3',
               'Def_y.3', 'WAR_y.3', 'BB%_x.5', 'K%_x.5', 'ISO_x.4', 'BABIP_x.5', 'AVG_x.5', 'OBP_x.4', 'SLG_x.4',
               'wOBA_x.4', 'wRC+_x.4', 'BsR_x.4', 'Off_x.4', 'Def_x.4', 'WAR_x.4', 'BB%_y.5', 'K%_y.5', 'ISO_y.4',
               'BABIP_y.5', 'AVG_y.5', 'OBP_y.4', 'SLG_y.4', 'wOBA_y.4', 'wRC+_y.4', 'BsR_y.4', 'Off_y.4', 'Def_y.4',
               'WAR_y.4', 'BB%_x.6', 'K%_x.6', 'ISO_x.5', 'BABIP_x.6', 'AVG_x.6', 'OBP_x.5', 'SLG_x.5', 'wOBA_x.5',
               'wRC+_x.5', 'BsR_x.5', 'Off_x.5', 'Def_x.5', 'WAR_x.5', 'BB%_y.6', 'K%_y.6', 'ISO_y.5', 'BABIP_y.6',
               'AVG_y.6', 'OBP_y.5', 'SLG_y.5', 'wOBA_y.5', 'wRC+_y.5', 'BsR_y.5', 'Off_y.5', 'Def_y.5', 'WAR_y.5',
               'BB%_x.7', 'K%_x.7', 'ISO_x.6', 'BABIP_x.7', 'AVG_x.7', 'OBP_x.6', 'SLG_x.6', 'wOBA_x.6', 'wRC+_x.6',
               'BsR_x.6', 'Off_x.6', 'Def_x.6', 'WAR_x.6', 'BB%_y.7', 'K%_y.7', 'ISO_y.6', 'BABIP_y.7', 'AVG_y.7',
               'OBP_y.6', 'SLG_y.6', 'wOBA_y.6', 'wRC+_y.6', 'BsR_y.6', 'Off_y.6', 'Def_y.6', 'WAR_y.6', 'BB%_x.8',
               'K%_x.8', 'ISO_x.7', 'BABIP_x.8', 'AVG_x.8', 'OBP_x.7', 'SLG_x.7', 'wOBA_x.7', 'wRC+_x.7', 'BsR_x.7',
               'Off_x.7', 'Def_x.7', 'WAR_x.7', 'BB%_y.8', 'K%_y.8', 'ISO_y.7', 'BABIP_y.8', 'AVG_y.8', 'OBP_y.7',
               'SLG_y.7', 'wOBA_y.7', 'wRC+_y.7', 'BsR_y.7', 'Off_y.7', 'Def_y.7', 'WAR_y.7', 'BB%_x.9', 'K%_x.9',
               'ISO_x.8', 'BABIP_x.9', 'AVG_x.9', 'OBP_x.8', 'SLG_x.8', 'wOBA_x.8', 'wRC+_x.8', 'BsR_x.8', 'Off_x.8',
               'Def_x.8', 'WAR_x.8', 'BB%_y.9', 'K%_y.9', 'ISO_y.8', 'BABIP_y.9', 'AVG_y.9', 'OBP_y.8', 'SLG_y.8',
               'wOBA_y.8', 'wRC+_y.8', 'BsR_y.8', 'Off_y.8', 'Def_y.8', 'WAR_y.8', 'wOBA', 'pickup_woy', 'ARI', 'ATL',
               'BAL', 'BOS', 'CHC', 'CIN', 'CLE', 'COL', 'CWS', 'DET', 'HOU', 'KC', 'LAA', 'LAD', 'MIA', 'MIL', 'MIN',
               'NYM', 'NYY', 'OAK', 'PHI', 'PIT', 'SD', 'SEA', 'SF', 'STL', 'TB', 'TEX', 'TOR', 'WSH']
        a.append(df.iloc[-1][col].values.tolist())
        train_x = pd.DataFrame(a, columns=col)
        #print(train_x)
        train_x['prediction'] = pd.DataFrame(clf2.predict(train_x))
        #df.to_csv('./prediction.csv',index= 0)
        #print('預測結果儲存完成')
        new.append(train_x['prediction'].values.tolist())
        print(new)
    df2['prediction'] = pd.DataFrame(list(new))
    df_finall = df2[['date','team_home','team_away','total','over','under','prediction']].copy()
    df_finall.to_csv('./pre_test.csv', mode='a', header=False,index=False)
