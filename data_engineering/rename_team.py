import pandas as pd

new_home = []
new_away = []
x = (new_home,new_away)
column_list = ['team_home','team_away']
def team_rename(name):
    if name == "Los Angeles Dodgers":
        return "LAD"
    if name == "Boston Red Sox":
        return "BOS"
    if name == "Milwaukee Brewers":
        return "MIL"
    if name == "Houston Astros":
        return "HOU"
    if name == "New York Yankees":
        return "NYY"
    if name == "Atlanta Braves":
        return "ATL"
    if name == "Cleveland Indians":
        return "CLE"
    if name == "Colorado Rockies":
        return "COL"
    if name == "Chicago Cubs":
        return "CHC"
    if name == "Kansas City Royals":
        return "KC"
    if name == "Seattle Mariners":
        return "SEA"
    if name == "San Diego Padres":
        return "SD"
    if name == "New York Mets":
        return "NYM"
    if name == "Minnesota Twins":
        return "MIN"
    if name == "Cincinnati Reds":
        return "CIN"
    if name == "Los Angeles Angels":
        return "LAA"
    if name == "San Francisco Giants":
        return "SF"
    if name == "Philadelphia Phillies":
        return "PHI"
    if name == "Baltimore Orioles":
        return "BAL"
    if name == "Arizona Diamondbacks":
        return "ARI"
    if name == "Chicago White Sox":
        return "CWS"
    if name == "St. Louis Cardinals" or name == "St.Louis Cardinals":
        return "STL"
    if name == "Toronto Blue Jays":
        return "TOR"
    if name == "Washington Nationals":
        return "WSH"
    if name == "Oakland Athletics":
        return "OAK"
    if name == "Texas Rangers":
        return "TEX"
    if name == "Pittsburgh Pirates":
        return "PIT"
    if name == "Miami Marlins" or name == "Florida Marlins":
        return "MIA"
    if name == "Detroit Tigers":
        return "DET"
    if name == "Tampa Bay Rays":
        return "TB"
    else:
        print("No name match found for "+name)
        return ""
def re_name_total(name):
    if name >= 6.5:
        print(name + 'is over value')
        return ''
    else:
        return name

if __name__ == '__main__':
    a = pd.read_csv('total_data.csv',index_col=0)
    for i in a['team_home']:
        b = team_rename(i)
        new_home.append(b)
    for j in a['team_away']:
        c = team_rename(j)
        new_away.append(c)
    print(new_away)
    print(new_home)
    data2 = pd.DataFrame({'team_home':new_home , 'team_away':new_away})
    a[['team_home','team_away']] = data2[['team_home','team_away']]
    a.to_csv('./total_data.csv', encoding='utf_8_sig')