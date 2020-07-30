import pandas as pd
import pymysql
import numpy as np



def DE(df):

    sea = []
    tm_home = []
    tm_away = []
    for season,tm in zip(df['date'],df['matchup']):
        sea.append(season[0:4])
        tm_home.append(tm.split('@')[1])
        tm_away.append(tm.split('@')[0])

    df['team_home'] = pd.DataFrame(tm_home)
    df['team_away'] = pd.DataFrame(tm_away)
    df['season'] = pd.DataFrame(sea)
    df.drop(['matchup','1top','2top','3top','4top','5top','1bot','2bot','3bot','4bot','5bot'],axis=1,inplace=True)
    print(df)
    #df.to_csv('./data/row_data_v1.csv',index=False)



    db = pymysql.connect(host='34.80.186.211',user='balao1312'\
                         ,passwd='clubgogo',db='MoneyBallDatabase', port=3306, charset='utf8')
    cursor = db.cursor() #建立游標
    sql_str='select * from umpire_data'
    cursor.execute(sql_str)
    df_umpire = pd.DataFrame(cursor.fetchall(),columns=['sid','Umpire','Games','K/BB'])
    db.close()

    df = pd.merge(df, df_umpire, left_on=['Umpires'],
                  right_on=['Umpire'],how='left').\
        drop(['Games','sid','Umpire','Umpires','Venue'] , axis=1)
    print(df)




    #從 mysql 讀 id_reference 的 table
    db = pymysql.connect(host='34.80.186.211',user='balao1312'\
                         ,passwd='clubgogo',db='MoneyBallDatabase', port=3306, charset='utf8')

    cursor = db.cursor() #建立游標

    sql_str='select * from pitcher_stats_v1'
    cursor.execute(sql_str)
    col = [des[0] for des in cursor.description]
    df_pitcher = pd.DataFrame(cursor.fetchall(),columns=col)
    #df_pitcher.to_csv('pitcher.csv', encoding='utf8', index=False)

    sql_str='select * from batter_score'
    cursor.execute(sql_str)
    col = [des[0] for des in cursor.description]
    df_batter = pd.DataFrame(cursor.fetchall(),columns=col)
    #df_batter.to_csv('batter.csv', encoding='utf8', index=False)

    db.close()

    #已經讀過存檔，直接從檔案讀
    #df_game = pd.read_csv('./data/row_data_v2.csv')
    # print(df_game)
    # print(df_game.columns)
    demo2 = []
    error = []
    for info in df.values.tolist():
        try:
            s = int(info[0][0:4])-1 #比賽日期抓年份
            # game表格home_pitcher欄位搜尋pitcher表格id
            i_home = df_pitcher[df_pitcher['mlb_id'].isin([str(info[5])]) &
                                df_pitcher['Season'].isin([str(s)])]
            data_home = i_home.fillna(0)
            # game表格away_pitcher欄位搜尋pitcher表格id
            i_away = df_pitcher[df_pitcher['mlb_id'].isin([str(info[4])]) &
                                df_pitcher['Season'].isin([str(s)])]
            data_away = i_away.fillna(0)
            #home_pitcher資料
            h_FB = data_home['FB'].values[0]
            h_SL = data_home['SL'].values[0]
            h_CT = data_home['CT'].values[0]
            h_CB = data_home['CB'].values[0]
            h_CH = data_home['CH'].values[0]
            h_SF = data_home['SF'].values[0]
            h_KN = data_home['KN'].values[0]
            batter_away = [info[6],info[7],info[8],info[9],info[10],info[11],
                           info[12],info[13],info[14]] #game表格所有客隊打者id
            type = ['FB','SL','CT','CB','CH','SF','KN']
            h_val = [h_FB,h_SL,h_CT,h_CB,h_CH,h_SF,h_KN]

            # away_pitcher資料
            a_FB = data_home['FB'].values[0]
            a_SL = data_home['SL'].values[0]
            a_CT = data_home['CT'].values[0]
            a_CB = data_home['CB'].values[0]
            a_CH = data_home['CH'].values[0]
            a_SF = data_home['SF'].values[0]
            a_KN = data_home['KN'].values[0]
            batter_home = [info[15], info[16], info[17], info[18], info[19],
                           info[20], info[21], info[22],info[23]]  # game表格所有客隊打者id
            a_val = [a_FB, a_SL, a_CT, a_CB, a_CH, a_SF, a_KN]


            demo_home = []
            demo_away = []
            #處理客隊打者資料
            for b in batter_away:
                x = []
                for p,q in zip(type,h_val):
                    #依照game表格搜尋到的打者id/年份/球種，對應batter表格打者成績
                    batter2 = df_batter[df_batter['player'].isin([b])
                                        & df_batter['season'].isin([str(s)])
                                        & df_batter['pitch_type'].isin([p])]
                    value= batter2['score'].values *float(q)
                    x.append(value)
                df = pd.DataFrame(x).replace('',0.1407142857142857) #空值補中位數
                try:
                    y = df.sum().values[0]
                except:
                    y = 0.1407142857142857
                demo_away.append(y)

            # 處理主隊打者資料
            for b in batter_home:
                z = []
                for p,q in zip(type,a_val):
                    #依照game表格搜尋到的打者id/年份/球種，對應batter表格打者成績
                    batter2 = df_batter[df_batter['player'].isin([b]) &
                                        df_batter['season'].isin([str(s)])&
                                        df_batter['pitch_type'].isin([p])]
                    value= batter2['score'].values *float(q)
                    z.append(value)
                df = pd.DataFrame(z).replace('',0.1407142857142857) #空值補中位數
                try:
                    y = df.sum().values[0]
                except:
                    y = 0.1407142857142857
                demo_home.append(y)

            all = [info[0],info[26],info[24],info[25],info[27],info[1],info[3],info[2],info[4],info[5],info[6],info[7],info[8],
                   info[9],info[10],info[11],info[12],info[13],info[14],info[15],info[16],info[17],info[18],info[19],info[20],
                   info[21],info[22],info[23],demo_away[0],demo_away[1],demo_away[2],demo_away[3],demo_away[4],demo_away[5],
                   demo_away[6],demo_away[7],demo_away[8],demo_home[0],demo_home[1],demo_home[2],demo_home[3],demo_home[4],
                   demo_home[5],demo_home[6],demo_home[7],demo_home[8]]
            #info[25] = away_total
            #info[24] = home_total
            #info[26] = yard_wOBA
            #info[29] = umpire_K/BB
            col = ['date','season','team_home','team_away','umpire_K/BB','game_time','away_total','home_total',
                   'away_pitcher','home_pitcher','a_1','a_2','a_3','a_4','a_5','a_6','a_7','a_8','a_9','h_1','h_2',
                   'h_3','h_4','h_5','h_6','h_7','h_8','h_9','a_v_1','a_v_2','a_v_3','a_v_4','a_v_5','a_v_6','a_v_7',
                   'a_v_8','a_v_9','h_v_1','h_v_2','h_v_3','h_v_4','h_v_5','h_v_6','h_v_7','h_v_8','h_v_9']
            demo2.append(all)
            print(len(demo2))



        except Exception as e:
            print(e)
            error.append(e)
            error.append(info)
            pass


    new_df = pd.DataFrame(demo2,columns=col)
    print('共%d筆資料遺失'%len(error))




    db = pymysql.connect(host='34.80.186.211',user='balao1312'\
                         ,passwd='clubgogo',db='MoneyBallDatabase', port=3306, charset='utf8')
    cursor = db.cursor() #建立游標
    sql_str='select * from pitcher_detail'
    cursor.execute(sql_str)
    col = [des[0] for des in cursor.description]
    pitcher_detail = pd.DataFrame(cursor.fetchall(),columns=col)


    sql_str='select * from batter_detail'
    cursor.execute(sql_str)
    col = [des[0] for des in cursor.description]
    batter_detail = pd.DataFrame(cursor.fetchall(),columns=col)
    new_df.to_csv('./bugggggggg.csv',index=False)

    db.close()

    sea2=[]
    for i in new_df.season:
        sea2.append(str(int(i)-1))
    new_df['merge_season'] = pd.DataFrame(sea2)

    new_df.away_pitcher = new_df.away_pitcher.astype(str)
    new_df.home_pitcher = new_df.home_pitcher.astype(str)
    pitcher_detail.Name = pitcher_detail.Name.astype(str)
    pitcher_detail.season = pitcher_detail.season.astype(str)
    batter_detail.Name = batter_detail.Name.astype(str)
    batter_detail.season = batter_detail.season.astype(str)
    new_df.drop('season',axis=1,inplace=True)
    new_df = pd.merge(new_df, pitcher_detail, left_on=['away_pitcher', 'merge_season'], right_on=['Name', 'season'],
                           how='left',suffixes=('_x', '_y')).drop(['away_pitcher','Name','Team','season'], axis=1)
    new_df = pd.merge(new_df, pitcher_detail, left_on=['home_pitcher', 'merge_season'], right_on=['Name', 'season'],
                           how='left',suffixes=('_x', '_y')).drop(['home_pitcher','Name','Team','season'], axis=1)

    for i in range (1,10):
        new_df["a_%s" % i] = new_df["a_%s" % i].astype(str)
        new_df["h_%s" % i] = new_df["h_%s" % i].astype(str)
        new_df = pd.merge(new_df, batter_detail, left_on=["a_%s" % i, 'merge_season'], right_on=['Name', 'season'],
                               how='left',suffixes=('_x', '_y')).drop(["a_%s"%i,'Team','season','Name' ], axis=1)
        new_df = pd.merge(new_df, batter_detail, left_on=["h_%s" % i, 'merge_season'], right_on=['Name', 'season'],
                               how='left',suffixes=('_x', '_y')).drop(["h_%s" % i,'Team','season','Name'], axis=1)
    new_df.drop('merge_season',axis=1,inplace=True)


    from work.weather_scripe import scrapy_weather
    weather_data = scrapy_weather()
    print(weather_data)
    weather_data['Fight_date'] = weather_data['Fight_date'].astype(str)
    weather_data['Fight_team1'] = weather_data['Fight_team1'].astype(str)
    weather_data['Fight_team2'] = weather_data['Fight_team2'].astype(str)
    new_df['date'] = pd.to_datetime(new_df['date'], format="%Y-%m-%d")
    new_df['date'] = new_df['date'].astype(str)
    new_df.team_home = new_df.team_home.astype(str)
    new_df.team_away = new_df.team_away.astype(str)


    new_df = pd.merge(new_df, weather_data, left_on=['date', 'team_home','team_away'], right_on=['Fight_date', 'Fight_team2','Fight_team1'],
                           how='left').drop(['Fight_date','Fight_team1','Fight_team2'], axis=1)
    new_df.drop_duplicates(subset=None, keep='first', inplace=True)



    #new_df = pd.read_csv('./demo_v3.csv')
    from work.odds_scrapy import odds_scarpy
#    odds = pd.read_csv('./odds.csv')
    odds = odds_scarpy()
#    odds.to_csv('./odds.csv',index=False)
    import datetime
    odds['date'] = odds['date'].apply(lambda x:datetime.datetime.strptime(x, "%d %b  %Y").strftime("%Y/%m/%d"))
    odds['date'] = pd.to_datetime(odds['date'], format="%Y/%m/%d")
    odds.date = odds.date.astype(str)
    print(odds)

    new_df['date'] = pd.to_datetime(new_df['date'], format="%Y/%m/%d")
    new_df['date'] = new_df['date'].astype(str)
    print(new_df)
    new_df = pd.merge(new_df, odds, on=['date', 'team_home','team_away'],how='left')
    new_df.drop(['K-BB%_x', 'K-BB%_y'], axis=1, inplace=True)
    #new_df.to_csv('./finall_data.csv', index=0)



    # #空值填補中位數
    # na_fill = ['a_v_1','a_v_2','a_v_3','a_v_4','a_v_5','a_v_6','a_v_7','a_v_8','a_v_9',
    #            'h_v_1','h_v_2','h_v_3','h_v_4','h_v_5','h_v_6','h_v_7','h_v_8','h_v_9','umpire_K/BB']
    # #df = pd.read_csv('./demo_v4.csv',na_values='0')
    # for i in na_fill:
    #     q_50 = np.percentile(new_df[~new_df[i].isnull()][i], 50)
    #     new_df.loc[new_df[i].isnull(),i] = q_50
    #     print(q_50)
    #     print(new_df)
    # new_df.fillna(0,inplace=True)
    # new_df.to_csv('finall_data.csv', encoding='utf8', index=False)
    #
    #
    #
    # na_fill=['K/9_x', 'BB/9_x', 'K/BB_x', 'HR/9_x', 'K%_x', 'BB%_x', 'AVG_x', 'WHIP_x', 'BABIP_x', 'LOB%_x',
    #          'ERA-_x', 'FIP-_x', 'xFIP-_x', 'ERA_x', 'FIP_x', 'E-F_x', 'xFIP_x', 'SIERA_x', 'K/9_y', 'BB/9_y', 'K/BB_y',
    #          'HR/9_y', 'K%_y', 'BB%_y', 'AVG_y', 'WHIP_y', 'BABIP_y', 'LOB%_y', 'ERA-_y', 'FIP-_y', 'xFIP-_y',
    #          'ERA_y', 'FIP_y', 'E-F_y', 'xFIP_y', 'SIERA_y', 'BB%_x.1', 'K%_x.1', 'ISO_x', 'BABIP_x.1', 'AVG_x.1', 'OBP_x',
    #          'SLG_x', 'wOBA_x', 'wRC+_x', 'BsR_x', 'Off_x', 'Def_x', 'WAR_x', 'BB%_y.1', 'K%_y.1', 'ISO_y', 'BABIP_y.1',
    #          'AVG_y.1', 'OBP_y', 'SLG_y', 'wOBA_y', 'wRC+_y', 'BsR_y', 'Off_y', 'Def_y', 'WAR_y', 'BB%_x.2', 'K%_x.2',
    #          'ISO_x.1', 'BABIP_x.2', 'AVG_x.2', 'OBP_x.1', 'SLG_x.1', 'wOBA_x.1', 'wRC+_x.1', 'BsR_x.1', 'Off_x.1',
    #          'Def_x.1', 'WAR_x.1', 'BB%_y.2', 'K%_y.2', 'ISO_y.1', 'BABIP_y.2', 'AVG_y.2', 'OBP_y.1', 'SLG_y.1',
    #          'wOBA_y.1', 'wRC+_y.1', 'BsR_y.1', 'Off_y.1', 'Def_y.1', 'WAR_y.1', 'BB%_x.3', 'K%_x.3', 'ISO_x.2',
    #          'BABIP_x.3', 'AVG_x.3', 'OBP_x.2', 'SLG_x.2', 'wOBA_x.2', 'wRC+_x.2', 'BsR_x.2', 'Off_x.2', 'Def_x.2',
    #          'WAR_x.2', 'BB%_y.3', 'K%_y.3', 'ISO_y.2', 'BABIP_y.3', 'AVG_y.3', 'OBP_y.2', 'SLG_y.2', 'wOBA_y.2',
    #          'wRC+_y.2', 'BsR_y.2', 'Off_y.2', 'Def_y.2', 'WAR_y.2', 'BB%_x.4', 'K%_x.4', 'ISO_x.3', 'BABIP_x.4',
    #          'AVG_x.4', 'OBP_x.3', 'SLG_x.3', 'wOBA_x.3', 'wRC+_x.3', 'BsR_x.3', 'Off_x.3', 'Def_x.3', 'WAR_x.3',
    #          'BB%_y.4', 'K%_y.4', 'ISO_y.3', 'BABIP_y.4', 'AVG_y.4', 'OBP_y.3', 'SLG_y.3', 'wOBA_y.3', 'wRC+_y.3',
    #          'BsR_y.3', 'Off_y.3', 'Def_y.3', 'WAR_y.3', 'BB%_x.5', 'K%_x.5', 'ISO_x.4', 'BABIP_x.5', 'AVG_x.5',
    #          'OBP_x.4', 'SLG_x.4', 'wOBA_x.4', 'wRC+_x.4', 'BsR_x.4', 'Off_x.4', 'Def_x.4', 'WAR_x.4', 'BB%_y.5',
    #          'K%_y.5', 'ISO_y.4', 'BABIP_y.5', 'AVG_y.5', 'OBP_y.4', 'SLG_y.4', 'wOBA_y.4', 'wRC+_y.4', 'BsR_y.4',
    #          'Off_y.4', 'Def_y.4', 'WAR_y.4', 'BB%_x.6', 'K%_x.6', 'ISO_x.5', 'BABIP_x.6', 'AVG_x.6', 'OBP_x.5',
    #          'SLG_x.5', 'wOBA_x.5', 'wRC+_x.5', 'BsR_x.5', 'Off_x.5', 'Def_x.5', 'WAR_x.5', 'BB%_y.6', 'K%_y.6',
    #          'ISO_y.5', 'BABIP_y.6', 'AVG_y.6', 'OBP_y.5', 'SLG_y.5', 'wOBA_y.5', 'wRC+_y.5', 'BsR_y.5', 'Off_y.5',
    #          'Def_y.5', 'WAR_y.5', 'BB%_x.7', 'K%_x.7', 'ISO_x.6', 'BABIP_x.7', 'AVG_x.7', 'OBP_x.6', 'SLG_x.6',
    #          'wOBA_x.6', 'wRC+_x.6', 'BsR_x.6', 'Off_x.6', 'Def_x.6', 'WAR_x.6', 'BB%_y.7', 'K%_y.7', 'ISO_y.6',
    #          'BABIP_y.7', 'AVG_y.7', 'OBP_y.6', 'SLG_y.6', 'wOBA_y.6', 'wRC+_y.6', 'BsR_y.6', 'Off_y.6', 'Def_y.6',
    #          'WAR_y.6', 'BB%_x.8', 'K%_x.8', 'ISO_x.7', 'BABIP_x.8', 'AVG_x.8', 'OBP_x.7', 'SLG_x.7', 'wOBA_x.7',
    #          'wRC+_x.7', 'BsR_x.7', 'Off_x.7', 'Def_x.7', 'WAR_x.7', 'BB%_y.8', 'K%_y.8', 'ISO_y.7', 'BABIP_y.8',
    #          'AVG_y.8', 'OBP_y.7', 'SLG_y.7', 'wOBA_y.7', 'wRC+_y.7', 'BsR_y.7', 'Off_y.7', 'Def_y.7', 'WAR_y.7',
    #          'BB%_x.9', 'K%_x.9', 'ISO_x.8', 'BABIP_x.9', 'AVG_x.9', 'OBP_x.8', 'SLG_x.8', 'wOBA_x.8', 'wRC+_x.8',
    #          'BsR_x.8', 'Off_x.8', 'Def_x.8', 'WAR_x.8', 'BB%_y.9', 'K%_y.9', 'ISO_y.8', 'BABIP_y.9', 'AVG_y.9',
    #          'OBP_y.8', 'SLG_y.8', 'wOBA_y.8', 'wRC+_y.8', 'BsR_y.8', 'Off_y.8', 'Def_y.8', 'WAR_y.8', 'wOBA']
    # df = pd.read_csv('./finall_data.csv',na_values=0)
    # df.drop(['K-BB%_x','K-BB%_y'],axis = 1 ,inplace=True)
    # for i in na_fill:
    #     try:
    #         q_50 = np.percentile(df[~df[i].isnull()][i], 50)
    #         df.loc[df[i].isnull(),i] = q_50
    #     except Exception as e :
    #         print(i)
    #         print(e)
    #         continue
    # df.fillna(0, inplace=True)
    # print(df)
    new_df.drop_duplicates(subset=['date','team_home','team_away'], keep='first', inplace=True)
    print(new_df)
    new_df.to_csv('finall_data.csv', encoding='utf8', index=False)
    return (new_df)









