import pandas as pd
import numpy as np

merged = pd.read_csv("data/merged_data.csv")

def featureEngineer(df):
    addMinutesPerGame(df)
    add_injury_history(df)
    add_avg_days_out_last_3(df)
    df = combine_same_seasons(df)
    dropColumns(df)
    return df

def dropColumns(df):
    df.drop('SEASON', axis=1, inplace=True)
    df.drop('POINTS_SCORED', axis=1, inplace=True)
    df.drop('PLAYER_NAME', axis=1, inplace=True)

def addMinutesPerGame(df):
    df['MPG'] = df['MINUTES_PLAYED'] / df['GAMES_PLAYED']

def add_injury_history(df):
    df["SEASON"] = df["SEASON"].astype(str).str.slice(0, 4).astype(int)
    
    df.sort_values(["PLAYER_NAME", "SEASON"], inplace=True)
    
    df["injury_event"] = 1
    
    def count_last_3_seasons(group):
        result = []
        for i in range(len(group)):
            season = group.iloc[i]["SEASON"]
            window = group[
                (group["SEASON"] >= season - 3) &
                (group["SEASON"] < season)
            ]
            result.append(window["injury_event"].sum())
        return pd.Series(result, index=group.index)
    
    # Fix: Add include_groups=False to silence the warning
    df["injuries_last_3"] = (
        df.groupby("PLAYER_NAME", group_keys=False)
          .apply(count_last_3_seasons, include_groups=False)
    )
    df.drop('injury_event', axis=1, inplace=True)

def add_avg_days_out_last_3(df):
    df.sort_values(["PLAYER_NAME", "SEASON"], inplace=True)
    
    def calc_avg_days_last_3_seasons(group):
        result = []
        for i in range(len(group)):
            season = group.iloc[i]["SEASON"]
            window = group[
                (group["SEASON"] >= season - 3) &
                (group["SEASON"] < season)
            ]
            # Calculate average days out for injuries in the window
            if len(window) > 0 and window["DAYS_OUT"].sum() > 0:
                avg_days = window["DAYS_OUT"].mean()
            else:
                avg_days = 0  # No injuries in last 3 seasons
            result.append(avg_days)
        return pd.Series(result, index=group.index)
    
    # Add new column in-place
    df["avg_days_out_last_3"] = (
        df.groupby("PLAYER_NAME", group_keys=False)
          .apply(calc_avg_days_last_3_seasons, include_groups=False)
    )

def combine_same_seasons(df):
    # Group by PLAYER_NAME and SEASON, sum DAYS_OUT, and take first value for other columns
    agg_dict = {'DAYS_OUT': 'sum'}
    
    # For all other columns (except PLAYER_NAME and SEASON), take the first value
    for col in df.columns:
        if col not in ['PLAYER_NAME', 'SEASON', 'DAYS_OUT']:
            agg_dict[col] = 'first'
    
    df_combined = df.groupby(['PLAYER_NAME', 'SEASON'], as_index=False).agg(agg_dict)
    
    return df_combined

merged = featureEngineer(merged)
merged.to_csv("./data/features_data.csv", index=False)


#print(merged.head(10))

#NEED TO ENGINEER
# Minutes Per Game | DONE
# Number of injuries in last 3 seasons | DONE
# Average duration for injury last 3 seasons | DONE

#FEATURES TO HAVE - EACH ENTRY IS A PLAYER SEASON
# HEIGHT
# WEIGHT
# POSITION
# GAMES PLAYED LAST SEASON
# GAMES STARTED LAST SEASON
# DAYS SPENT ON IL
# MINUTES PLAYED LAST SEASON
# AGE
# MINUTES PER GAME LAST SEASON
# NUM OF INJURIES IN LAST 3 SEASONS
# AVG DURATION FOR INJURY
