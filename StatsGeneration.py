import nba_api.stats.endpoints as nba
import pandas
import pandas as pd
import numpy as np
import matplotlib as plot
#import tensorflow as tf
from nba_api.stats.static import teams,players

#In this file, I want to be able to make a couple spreadsheets of Hawks players
#Along with the team stats for each game in the 2018-2019 season. I want to be able
#make some advanced stat calculations and see if I can find the best combination of stats
#check in order to best fit a model that uses weighted averages to accurately predict
#the points a player will score on a given day.

#first lets grab players

#Retrieving active player information for each season
years=list(range(2003,2024))
players=players.get_active_players()
seasons=[]
for index,year in enumerate(years):
    try:
        seasons.append(str(year)+'-'+str(years[index+1])[2:4])
    except IndexError:
        break
print(seasons)
lebron_id=[player['id'] for player in players if player['full_name']=='LeBron James'][0]
game_ids=[]
for season_num in seasons:
    cur_season=nba.CommonAllPlayers(is_only_current_season=0,season=season_num).get_data_frames()[0]
    cur_season=cur_season[cur_season['ROSTERSTATUS']==1]
    #cur_season=all active players in that season

    #********Refer to here for easy team box score calculations************

    if lebron_id in cur_season['PERSON_ID'].values:
        season_team=cur_season['TEAM_ID'][cur_season['PERSON_ID']==lebron_id]
        games=nba.leaguegamefinder.LeagueGameFinder(team_id_nullable=season_team, season_nullable=season_num, season_type_nullable='Regular Season').get_data_frames()[0]
        game_ids.append(games['GAME_ID'].values)
    #games=all games target player's current team played (including target player DNP)

#Most basic approach: Prediction based off of own player stats
#X data is going to be completely based off of target player's stats in each box s
#Making list of game ids
game_ids=np.concatenate(game_ids)
print(game_ids)
lebron_data=pd.DataFrame()
for id in game_ids:
    boxScore=nba.BoxScoreTraditionalV2(game_id=id).get_data_frames()[0]
    lebron_stats=boxScore[boxScore['PLAYER_ID']==lebron_id]
    lebron_data=pd.concat([lebron_data, lebron_stats])
    lebron_data.to_excel('lebron.xlsx')







