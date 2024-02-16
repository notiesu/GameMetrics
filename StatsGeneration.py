import nba_api.stats.endpoints as nba
from nba_api.stats.endpoints import commonallplayers
import pandas
import pandas as pd
import numpy as np
import matplotlib as plot

# import tensorflow as tf
from nba_api.stats.static import teams, players

"""In this file, I want to be able to make a couple spreadsheets of Hawks players
Along with the team stats for each game in the 2018-2019 season. I want to be able
make some advanced stat calculations and see if I can find the best combination of stats
check in order to best fit a model that uses weighted averages to accurately predict
the points a player will score on a given day."""

"""Set the years/seasons we want to retrieve"""
years = list(range(2003, 2024))

"""Retrieve the active players"""
players = players.get_active_players()

seasons = []


"""This loops through the years list and adds the year the season ends to the year in the list. e.g. 2008 becomes 2008-09"""
for index, year in enumerate(years):
    try:
        seasons.append(str(year) + "-" + str(years[index + 1])[2:4])
    except IndexError:
        break

"""Much easier to read way of finding the correct id"""
lebron_id = None
for player in players:
    if player["full_name"] == "LeBron James":
        lebron_id = player["id"]

game_ids = []

"""Using a function for readability and flexibility"""


def get_active_players_for_season(season_num):
    all_players = commonallplayers.CommonAllPlayers(
        is_only_current_season=0, season=season_num
    ).get_data_frames()[0]
    active_players = all_players[all_players["ROSTERSTATUS"] == 1]
    return active_players


seasons = ["2019-20", "2020-21"]
active_players_by_season = {}

for season_num in seasons:
    current_season = active_players_by_season[season_num] = (
        get_active_players_for_season(season_num)
    )

    if lebron_id in current_season["PERSON_ID"].values:
        season_team = current_season.loc[
            current_season["PERSON_ID"] == lebron_id, "TEAM_ID"
        ].iloc[0]
        games = nba.leaguegamefinder.LeagueGameFinder(
            team_id_nullable=season_team,
            season_nullable=season_num,
            season_type_nullable="Regular Season",
        ).get_data_frames()[0]
        game_ids.extend(games["GAME_ID"].values.tolist())

game_ids = np.array(game_ids)


print(game_ids)


lebron_data = pd.DataFrame()


for id in game_ids:
    boxScore = nba.BoxScoreTraditionalV2(game_id=id).get_data_frames()[0]
    lebron_stats = boxScore[boxScore["PLAYER_ID"] == lebron_id]
    lebron_data = pd.concat([lebron_data, lebron_stats])
    lebron_data.to_excel("lebron.xlsx")
