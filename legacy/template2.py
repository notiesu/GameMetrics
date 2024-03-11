from nba_api.stats.endpoints import (
    BoxScoreSummaryV2,
    BoxScoreTraditionalV2,
    BoxScoreAdvancedV2,
)
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd
import numpy as np
import matplotlib as plot

# import tensorflow as tf
from nba_api.stats.static import teams, players

############### Another template script. Might be used for reference, but otherwise deprecated.#######

nba_teams = teams.get_teams()
players = players.get_active_players()

# Select the dictionary for the Celtics, which contains their team ID
celtics = [team for team in nba_teams if team["abbreviation"] == "BOS"][0]
celtics_id = celtics["id"]
from nba_api.stats.endpoints import leaguegamefinder

# Query for games where the Celtics were playing
gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=celtics_id)
# The first DataFrame of those returned is what we want.
games = gamefinder.get_data_frames()[0]

# Trying to get all of the 2019 regular season game data
games_in_2019 = games[games.SEASON_ID == "22019"]
# Create datasets. We are going to try to predict the plus_minus of the next game based on previous game factors.
# Clean the datasets
# Ok so now I have the dataset in an excel file to so lets see how this goes
