import requests
from bs4 import BeautifulSoup
import pandas as pd
import pytz
import time
import csv
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def GAME_DATE(US_ET_date):
    MLB_url = f'https://www.mlb.com/starting-lineups/{US_ET_date}'
    # print(MLB_url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    req = requests.get(MLB_url , headers = headers)
    soup = BeautifulSoup(req.text , 'html.parser')

    #場次
    Number_of_games = len(soup.select('div[class="starting-lineups__game"]'))
    # print(Number_of_games)

    game_and_time_dic = {}
    for i in range(Number_of_games) :
        game_start_time = soup.select('div[class="starting-lineups__game-date-time"] time ')[i]['datetime'][11:16]
        get_30min_ago = datetime.datetime.strptime(game_start_time , '%H:%M') + datetime.timedelta(minutes= -30) + datetime.timedelta(hours=-4)
        game_start_time = str(get_30min_ago).split(' ')[1]
        game_and_time_dic[i] = game_start_time
    return game_and_time_dic,Number_of_games


def spider(index, gamedate, gametime):
    print('\nEnter spider')
    print(index,gamedate,gametime)
    url = f'https://www.mlb.com/starting-lineups/{gamedate}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    req = requests.get(url,headers = headers)
    soup = BeautifulSoup(req.text,'html.parser')

    check_status = soup.select('div[class="starting-lineups__game-details"] ')[index]
    check_status = check_status.select('div span[class="starting-lineups__game-state starting-lineups__game-state--postponed"]')

    if check_status != []:
        print('賽事延期或其他')
    else:
        return_list = []

        return_list.append(gamedate)
        return_list.append(gametime)


        '''
        matchup 
        '''
        away = soup.select('div[class="starting-lineups__game"]')[index].select('span[class="starting-lineups__team-name starting-lineups__team-name--away"] \
                                                                         a[class="starting-lineups__team-name--link"]')[0]['data-tri-code']
        home = soup.select('div[class="starting-lineups__game"]')[index].select('span[class="starting-lineups__team-name starting-lineups__team-name--home"] \
                                                                         a[class="starting-lineups__team-name--link"]')[0]['data-tri-code']
        matchup = f'{away}@{home}'
        # print(f'對戰組合:{matchup}')
        return_list.append(matchup)

        '''
        point
        '''
        for i in range(12):
            return_list.append(i)

        '''
        Umpires 
        '''
        Umpires = 'Joe West'
        return_list.append(Umpires)

        '''
        Venue
        '''
        Venue = soup.select('div[class="starting-lineups__game-location"]')[index].text.strip()
        # print(f'球場:{Venue}')
        return_list.append(Venue)

        '''
        pitcher 
        '''
        pitcher = soup.select('div[class="starting-lineups__pitchers"]')[index]
        try:
            away_pitcher = pitcher.select('div[class="starting-lineups__pitcher-name"] a')[0].text
            away_pitcher_ID = str(pitcher.select('div[class="starting-lineups__pitcher-name"] a')[0]['href'])[-6:]
            # print(f'客隊投手:{away_pitcher} ID:{away_pitcher_ID}')
            return_list.append(away_pitcher_ID)
        except EnvironmentError as a :
            print(a)
        try:
            home_pitcher = pitcher.select('div[class="starting-lineups__pitcher-name"] a')[1].text
            home_pitcher_ID = str(pitcher.select('div[class="starting-lineups__pitcher-name"] a')[1]['href'])[-6:]
            # print(f'主隊投手:{home_pitcher} ID:{home_pitcher_ID}')
            return_list.append(home_pitcher_ID)
        except EnvironmentError as a :
            print(a)


        '''
        先發打順 姓名、ID
        '''
        batter = soup.select('div[class="starting-lineups__teams starting-lineups__teams--xs starting-lineups__teams--md starting-lineups__teams--lg"]')[index]
        away_batter_list = []
        home_batter_list = []
        for i in range(9):
            away_batter_name = batter.select('a[class="starting-lineups__player--link"]')[i].text
            away_batter_ID = batter.select('a[class="starting-lineups__player--link"]')[i]['href'][-6:]
            away_batter_list += [away_batter_ID]
            return_list.append(away_batter_ID)

        for i in range(9,18):
            home_batter_name = batter.select('a[class="starting-lineups__player--link"]')[i].text
            home_batter_ID = batter.select('a[class="starting-lineups__player--link"]')[i]['href'][-6:]
            home_batter_list += [home_batter_ID]
            return_list.append(home_batter_ID)

        print(away_batter_list , home_batter_list)



        print('■■■■■■■■■■■■■■■■■■■■■■■■■■■■■')
        with open('./game/game{}.csv'.format(gamedate), 'a', newline='', encoding='utf-8-sig') as g:
            MLB_row = csv.writer(g)
            MLB_row.writerow(return_list)
        print(return_list)
        print('■■■■■■■■■■■■■■■■■■■■■■■■■■■■■')
    return pd.read_csv('./game/game{}.csv'.format(gamedate))





# option = webdriver.ChromeOptions()
#
# options = Options()
# prefs = {
#     'profile.default_content_setting_values':
#         {
#             'notifications': 2
#         }
# }
# options.add_experimental_option('prefs',prefs)
# options.add_argument('--headless')
# options.add_argument('blink-settings=imagesEnabled=false')
# options.add_argument("--disable-javascript")  # 禁用JavaScript
# options.add_argument('--disable-gpu')  # google say加上這個屬性來規避bug
# options.add_argument('--no-sandbox')  # 以最高權限運行
# options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome("./chromedriver.exe", options=options)
# driver.get(MLB_url)
# driver.quit()


if __name__ == '__main__':
    #GAME_DATE('2020-07-28')
    spider()