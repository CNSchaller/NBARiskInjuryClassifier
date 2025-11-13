import pandas as pd
import numpy as np
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo

def loadCleanedFile():
    df = pd.read_csv('data/injury_stats_clean.csv')
    return df

df_working = loadCleanedFile()

# Nikola Jokić
career = playercareerstats.PlayerCareerStats(player_id='203999')
df_1 = career.season_totals_regular_season.get_data_frame()
#print(df_1.head(10))
#print(df_1.columns.tolist())

#Columns returned:
#['PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 
# FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

#Wanted columns:
#GS - games started
#GP - games played
#MIN - minutes

other_stats = commonplayerinfo.CommonPlayerInfo(player_id='203999')
os_df = other_stats.common_player_info.get_data_frame()
#print(os_df.columns.tolist())

#Columns returned:
#['PERSON_ID', 'FIRST_NAME', 'LAST_NAME', 'DISPLAY_FIRST_LAST', 'DISPLAY_LAST_COMMA_FIRST', 'DISPLAY_FI_LAST', 'PLAYER_SLUG', 
# 'BIRTHDATE', 'SCHOOL', 'COUNTRY', 'LAST_AFFILIATION', 'HEIGHT', 'WEIGHT', 'SEASON_EXP', 'JERSEY', 'POSITION', 
# 'ROSTERSTATUS', 'GAMES_PLAYED_CURRENT_SEASON_FLAG', 'TEAM_ID', 'TEAM_NAME', 'TEAM_ABBREVIATION', 'TEAM_CODE', 'TEAM_CITY', 
# 'PLAYERCODE', 'FROM_YEAR', 'TO_YEAR', 'DLEAGUE_FLAG', 'NBA_FLAG', 'GAMES_PLAYED_FLAG', 'DRAFT_YEAR', 'DRAFT_ROUND', 'DRAFT_NUMBER', 
# 'GREATEST_75_FLAG']

# Wanted columns:
# AGE
# HEIGHT
# WEIGHT
# POSITION

#print(os_df.head(10))
