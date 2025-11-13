import pandas as pd
import numpy as np
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players

def loadCleanedFile():
    df = pd.read_csv('data/injury_stats_clean.csv')
    return df

def getPlayerID(name): #returns the players ID from the NBA api. some players have the same name, so need to add logic to handle that
    matching_players = players.find_players_by_full_name(name)
    return matching_players
    return matching_players[0]['id']

def getPlayersCareerStats(id):
    career = playercareerstats.PlayerCareerStats(player_id=id)
    dataframe = career.season_totals_regular_season.get_data_frame()
    return dataframe

def getPlayersCommonInfo(id):
    other_stats = commonplayerinfo.CommonPlayerInfo(player_id=id)
    dataframe = other_stats.common_player_info.get_data_frame()
    return dataframe



df_working = loadCleanedFile()
TatumsID = getPlayerID('Jabari Smith')
#TatumsCareer = getPlayersCareerStats(TatumsID)
#TatumsInfo = getPlayersCommonInfo(TatumsID)
print(TatumsID)

#EXAMPLE USAGES

#-----------HOW TO GET A PLAYERS PLAYERID----------
#player_name = "Michael Jordan"

#matching_players = players.find_players_by_full_name(player_name)
#print(matching_players[0]['id'])

#----------HOW TO GET PLAYERS CUMULATIVE CAREER STATS---------
# Nikola Jokić
#career = playercareerstats.PlayerCareerStats(player_id='203999')
#df_1 = career.season_totals_regular_season.get_data_frame()
#print(df_1.head(10))
#print(df_1.columns.tolist())

#Columns returned:
#['PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 
# FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

#Wanted columns:
#GS - games started
#GP - games played
#MIN - minutes
#PLAYER_AGE - players age at start of that season


#----------HOW TO GET PLAYERS COMMON INFORMATION----------
#other_stats = commonplayerinfo.CommonPlayerInfo(player_id='203999')
#os_df = other_stats.common_player_info.get_data_frame()
#print(os_df.columns.tolist())

#Columns returned:
#['PERSON_ID', 'FIRST_NAME', 'LAST_NAME', 'DISPLAY_FIRST_LAST', 'DISPLAY_LAST_COMMA_FIRST', 'DISPLAY_FI_LAST', 'PLAYER_SLUG', 
# 'BIRTHDATE', 'SCHOOL', 'COUNTRY', 'LAST_AFFILIATION', 'HEIGHT', 'WEIGHT', 'SEASON_EXP', 'JERSEY', 'POSITION', 
# 'ROSTERSTATUS', 'GAMES_PLAYED_CURRENT_SEASON_FLAG', 'TEAM_ID', 'TEAM_NAME', 'TEAM_ABBREVIATION', 'TEAM_CODE', 'TEAM_CITY', 
# 'PLAYERCODE', 'FROM_YEAR', 'TO_YEAR', 'DLEAGUE_FLAG', 'NBA_FLAG', 'GAMES_PLAYED_FLAG', 'DRAFT_YEAR', 'DRAFT_ROUND', 'DRAFT_NUMBER', 
# 'GREATEST_75_FLAG']

# Wanted columns:
# HEIGHT
# WEIGHT
# POSITION

#print(os_df.head(10))
