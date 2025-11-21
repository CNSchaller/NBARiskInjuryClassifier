import pandas as pd
import numpy as np

def load_file():
    df = pd.read_csv("data/player_stats.csv")
    return df

def clean_dataset(df):

    #Select columns that may be relevent for modeling
    df = df[['PLAYER_NAME_x','SEASON_ID','PLAYER_AGE','GP','GS','MIN','PTS','HEIGHT','WEIGHT','POSITION']]

    #rename columns for better readability
    df = df.rename(columns={
        "PLAYER_NAME_x": "PLAYER_NAME",
        "SEASON_ID": "SEASON",
        "PLAYER_AGE": "AGE",
        "GP": "GAMES_PLAYED",
        "GS": "GAMES_STARTED",
        "MIN": "MINUTES_PLAYED",
        "PTS": "POINTS_SCORED",
    })

    #print(df.head())

    #Remove duplicate rows
    df = df.drop_duplicates()
    duplicate_count = df.duplicated().sum()
    print("Total duplicate rows:", duplicate_count)

    #Handle missing values
    #GAMES_STARTED, HEIGHT, WEIGHT, POSTITION all have a number of missing values
    #WIll fill missing GAMES_STARTED with 0, as some players may not have started any games
    #Will remove rows where HEIGHT and WEIGHT are missing, as these are important for analysis
    #Will fill missing POSITION with 'Unknown'
    print(df.isnull().sum())
    df['GAMES_STARTED'] = df['GAMES_STARTED'].fillna(0)
    df = df.dropna(subset=['HEIGHT', 'WEIGHT'])
    df['POSITION'] = df['POSITION'].fillna('Unknown')

    #Check for datatypes of columns
    #Height is an object so lets convert it to int (inches)
    #print(df.info())

    def height_to_inches(h):
        feet, inches = h.split('-')
        return int(feet) * 12 + int(inches)
    
    df["HEIGHT"] = df["HEIGHT"].apply(height_to_inches)
    print(df.head())


    #Check for strange outliers in numeric columns
    #print(df.describe())

    return df

def main():
    df = load_file()
    df = clean_dataset(df)

    df.to_csv("data/player_stats_clean.csv", index=False)

if __name__ == "__main__":
    main()

