import requests
import pandas as pd
import pytz
import datetime


def scrapy_weather():
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    url = 'https://swishanalytics.com/mlb/weather'
    res = requests.get(url, headers=headers).content
    df = pd.read_html(res)
    data = pd.DataFrame(df[0])
    US_ET = pytz.timezone('US/Eastern')
    US_ET_datetime = str(datetime.datetime.now(US_ET)).split(' ')
    US_ET_date = US_ET_datetime[0]
    col = ['PA', 'wOBA', 'BA', 'OBP', 'SLG', 'H', '1B', '2B', '3B', 'HR', 'RBI',
           'BB', 'IBB', 'HBP', 'SO', 'SAC', 'SF', 'GIDP', 'GROUND', 'LINE', 'POP',
           'FLY', 'matchup', 'Fight_date']
    df_weather = []
    for i,j in zip((range(2,len(df),2)),(range(-1,len(data)))):
        if i == 2 :
            pass
        else:
            weather = pd.DataFrame(df[i])
            weather['matchup'] = data.iloc[j,1]
            weather['Fight_date'] = US_ET_date
            for k in weather.values.tolist():
                df_weather.append(k)
            #print(weather.columns)

    data = pd.DataFrame(df_weather,columns=col)
    print(data)
    df_weather = data[['Fight_date','wOBA','matchup']].copy()
    df_weather['Fight_team1'] = df_weather['matchup'].apply(lambda x:x.split('@')[0].replace(' ',''))
    df_weather['Fight_team2'] = df_weather['matchup'].apply(lambda x:x.split('@')[1].replace(' ',''))
    df_weather.drop('matchup',axis=1,inplace=True)
    return (df_weather)
