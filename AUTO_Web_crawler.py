import web_crawler
import pytz
import datetime
import pandas as pd
import csv
import time
from work.DE import DE
from web_crawler import spider



def AUTO_crawler():
    #check the ET
    while 1 :
        US_ET = pytz.timezone('US/Eastern')
        US_ET_datetime = str(datetime.datetime.now(US_ET)).split(' ')
        # print(US_ET_datetime)
        US_ET_date = US_ET_datetime[0]
        US_ET_time = US_ET_datetime[1].split('.')[0]
        US_ET_time_split = US_ET_time.split(':')[0:2]
        print(US_ET_date, US_ET_time)
        # print(US_ET_time.split(':')[0:2])
        # print('\n')

        column_list = ['date', 'time', 'matchup', '1top', '1bot', '2top', '2bot', '3top', '3bot', '4top', '4bot',
                       '5top', '5bot',
                       'away_total', 'home_total', 'Umpires', 'Venue',
                       'away_pitcher', 'home_pitcher',
                       'v_1', 'v_2', 'v_3', 'v_4', 'v_5', 'v_6', 'v_7', 'v_8', 'v_9',
                       'h_1', 'h_2', 'h_3', 'h_4', 'h_5', 'h_6', 'h_7', 'h_8', 'h_9']
        # with open('./game/game{}.csv'.format(US_ET_date), 'w', newline='', encoding='utf-8-sig') as f:
        #     MLB_clumn = csv.writer(f)
        #     MLB_clumn.writerow(column_list)


        #check換日
        game_date = open('date.txt', 'r', encoding='utf-8-sig').read()
        if  game_date != US_ET_date: #如果換日 會去爬取明天有幾場賽事 並將比賽時間用字典記下
            if US_ET_time_split == ['16','05'] :
                print(US_ET_time_split)
                print(f'{game_date} change to {US_ET_date}')
                open('date.txt', 'w', encoding='utf-8-sig').write(US_ET_date)
                game_date = US_ET_date
                print(f'{game_date} changed!!')
                return_dic = web_crawler.GAME_DATE(game_date)[0]
                return_len = web_crawler.GAME_DATE(game_date)[1]
                # print(type(return_dic),return_dic)
                # print(type(return_len),return_len)
                open('game_time.txt','w',encoding='utf-8-sig').write(str(return_dic))

                column_list = ['date', 'time', 'matchup', '1top', '1bot', '2top', '2bot', '3top', '3bot', '4top', '4bot',
                               '5top', '5bot',
                               'away_total', 'home_total', 'Umpires', 'Venue',
                               'away_pitcher', 'home_pitcher',
                               'v_1', 'v_2', 'v_3', 'v_4', 'v_5', 'v_6', 'v_7', 'v_8', 'v_9',
                               'h_1', 'h_2', 'h_3', 'h_4', 'h_5', 'h_6', 'h_7', 'h_8', 'h_9']
                with open('./game/game{}.csv'.format(US_ET_date), 'w', newline='', encoding='utf-8-sig') as f:
                    MLB_clumn = csv.writer(f)
                    MLB_clumn.writerow(column_list)

        elif game_date == US_ET_date:  #如果偵測到時間到了 會利用時間去找對應INDEX 爬取資訊
            gametime_dic = eval(open('game_time.txt','r',encoding='utf-8-sig').read())
            print(type(gametime_dic),gametime_dic)
            for i in gametime_dic:
                time_key = gametime_dic[i].split(':')[0:2]
                # print(time_key, US_ET_time_split)
                if time_key == US_ET_time_split:
                    print('right')
                    game = web_crawler.spider(i, US_ET_date, US_ET_time)
                    DE(game)
                    from work.prediction import modle_train
                    modle_train()
                    df_set = pd.read_csv('./pre_test.csv',na_values='')
                    df_set.drop_duplicates(subset=['date', 'team_home', 'team_away'], keep='last', inplace=True)
                    df_set.dropna(axis=0, how='any', inplace=True)
                    df_set.to_csv('./pre_test.csv', index=False)
                    print(df_set)
                    print('finish')


        else:
            print('ERROR')

        print('cool down\n')
        time.sleep(55)


        # #存賽事index跟開賽前30分
        # game_time_dic = web_crawler.GAME_DATE(US_ET_date)
        # with open('game_time.txt','a',encoding='utf-8-sig') as a:
        #     a.write(f'{game_time_dic}')

        column_list = ['date', 'time', 'matchup', '1top', '1bot', '2top', '2bot', '3top', '3bot', '4top', '4bot',
                       '5top', '5bot',
                       'away_total', 'home_total', 'Umpires', 'Venue',
                       'away_pitcher', 'home_pitcher',
                       'v_1', 'v_2', 'v_3', 'v_4', 'v_5', 'v_6', 'v_7', 'v_8', 'v_9',
                       'h_1', 'h_2', 'h_3', 'h_4', 'h_5', 'h_6', 'h_7', 'h_8', 'h_9']

        # df = pd.DataFrame(,columns=column_list)









if __name__ == '__main__':
    AUTO_crawler()
    #spider(0,'2020-07-28')