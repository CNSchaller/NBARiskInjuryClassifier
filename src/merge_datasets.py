import pandas as pd
import numpy as np


def main():
    player_data = pd.read_csv("data/player_stats_clean.csv")
    injury_data = pd.read_csv("data/injury_stats_clean.csv")

    #rename for easier merging
    injury_data.rename(columns={
        "Player": "PLAYER_NAME"
    }, inplace=True)

    #need to convert injury dates to seasons to match player data
    def date_to_season(date_string):
        date = pd.to_datetime(date_string)
        year = date.year
        if date.month >= 7:
            return f"{year}-{str(year+1)[-2:]}"
        else:
            return f"{year-1}-{str(year)[-2:]}"
    injury_data["SEASON"] = injury_data["Date Relinquished"].apply(date_to_season)
    injury_data.drop(columns=["Date Relinquished","Date Activated"], inplace=True)
    injury_data.rename(columns={"Days Out":"DAYS_OUT"}, inplace=True)

    merged_data = pd.merge(
        player_data,
        injury_data,
        on=["PLAYER_NAME", "SEASON"],
        how="left"
    )

    print(merged_data.head())

    #Check for duplicates
    duplicate_count = merged_data.duplicated().sum()
    #print("Total duplicate rows:", duplicate_count)

    #Check for missing values
    #Days Out has quite a number of missing values so we will remove these rows 
    print(merged_data.isnull().sum())
    merged_data = merged_data.dropna(subset=["DAYS_OUT"])

    #Check for datatypes of columns
    #Days_Out is object so lets convert it to float
    #print(merged_data.info())
    merged_data["DAYS_OUT"] = (merged_data["DAYS_OUT"].str.replace(" days", "", regex=False).astype(int))
    #print(merged_data.head())


    #Check for strange outliers in numeric columns
    #Days_out has a max value of 3295 lets check it out
    weird = merged_data[merged_data["DAYS_OUT"] > 365]
    print(weird)
    #lets remove these outliers for now
    merged_data = merged_data[merged_data["DAYS_OUT"] <= 365]
    print(merged_data.describe())


    # Create NEXT-SEASON Y (DAYS_OUT_NEXT)
    merged_data = merged_data.sort_values(by=["PLAYER_NAME", "SEASON"])

    merged_data["DAYS_OUT_NEXT"] = (
        merged_data.groupby("PLAYER_NAME")["DAYS_OUT"].shift(-1)
    )

    # Remove seasons where we don't have next season's injury data
    merged_data = merged_data.dropna(subset=["DAYS_OUT_NEXT"])

    # Drop current-season DAYS_OUT to prevent leakage
    merged_data = merged_data.drop(columns=["DAYS_OUT"])

    # Save cleaned + target-engineered dataset
    merged_data.to_csv("data/merged_data.csv", index=False)
    print(merged_data.head())




    merged_data.to_csv("data/merged_data.csv", index=False)

if __name__ == "__main__":
    main()

