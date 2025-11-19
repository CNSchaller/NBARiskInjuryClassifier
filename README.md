# Predicting NBA Injury Recovery Time

#### Team: Derrick White Fan Club
#### Members: Charlotte Hauke, Calvin Schaller



### Overview
This project aims to predict how long an NBA player will be out due to injury, measured in days missed ("Days Out").
Injuries have major impacts on player performance, team success, and season outcomes.
By building a data-driven regression model, we estimate recovery duration based on player workload, demographics, injury type, and history.
Our results can provide insights for teams, trainers, and analysts seeking to understand factors influencing recovery time.


### Datasets
1. NBA Injury Stats (1951–2023) – Kaggle https://www.kaggle.com/datasets/loganlauton/nba-injury-stats-1951-2023
- Approximately 37,000 entries
- Columns include player name, team, season, injury type, location, date, and games/days missed
- Provides historical records of NBA injuries
2. NBA Player Stats – Official NBA API https://www.NBA.com
- Player demographics: height, weight, age, position, team
- Performance metrics: minutes per game, usage rate, points, assists, rebounds, fouls
- Provides season-by-season workload and performance data

### Project Structure

```bash
NBARiskInjuryClassifier/
│
├── data/
│   ├── InjuryStats.csv           # Raw injury dataset from Kaggle
|   ├── injury_stats_clean.csv    # Cleaned injury dataset
|   ├── player_stats.csv          # Raw player stats from NBA API
|   ├── player_stats_clean.csv    # Clean player stats from NBA API
|   ├── merged_data.csv           # Merged injury and player data
│   └── features_data.csv         # Feature engineered dataset
│
├── src/
│   ├── injury_parser.py          # Reads and cleans raw InjuryStats.csv
|   ├── player_stats_fetch.py     # Reads and downloads player data from NBA API
|   ├── player_stats_parser.py    # cleans player data from NBA API
|   ├── merge_datasets.py         # Merges injury and player data
│   ├── features.py               # Feature engineering and transformations
│   └── train_model.py            # Model training and evaluation
│
├── notebooks/
│   ├── 01_EDA.ipynb              # Exploratory data analysis
│   └── 02_Modeling.ipynb         # Model experimentation and tuning
│
└── README.md                     # Project documentation
```
### Methods

### Results

### Key Insights

### How to Run
To access the nba api, the pandas, requests, and numpy packages are recquired. Run
```pip install nba_api```
before using the model.

### TO DO BEFORE MONDAY
- Clean player data (charlotte)
- Merge datasets (charlotte)
- Feature engineering (calvin)
- EDA (charlotte)
- Fit the model (and tweak if necessary) (calvin)
- Write report /poster


### References
