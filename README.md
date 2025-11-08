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
│   └── player_stats.csv          # Player stats from NBA API
│
├── src/
│   ├── parser.py                 # Cleans and merges raw datasets
|   ├── get_player_stats.py       # Pulls player stats from NBA API
│   ├── features.py               # Feature engineering and transformations
│   ├── train_model.py            # Model training and evaluation
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

### References
