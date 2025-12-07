# Predicting NBA Injury Recovery Time

#### Team: Derrick White Fan Club
#### Members: Charlotte Hauke, Calvin Schaller



### Overview
This project aims to predict how long an NBA player will be out due to injury in their nexr season, measured in days missed ("Days Out").
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
│   └── modeling.ipynb         # Model experimentation and tuning
│
└── README.md                     # Project documentation
```
### Methods

After merging and cleaning, our final dataset consisted of the following columns: PLAYER_NAME, SEASON, AGE, GAMES_PLAYED, GAMES_STARTED, MINUTES_PLAYED, POINTS_SCORED, HEIGHT, WEIGHT, POSITION, and DAYS_OUT_NEXT.

Initial exploratory data analysis revealed that many features were heavily skewed. For this reason, we chose a random forest regressor to predict our target. However, the first round of modeling produced a negative R² value, indicating that the model performed worse than simply predicting the mean.

To improve performance, we engineered additional features designed to capture more meaningful patterns and applied a log transformation to the target variable to reduce the impact of outliers. These changes led to improvements in both MSE and R².

Finally, we conducted hyperparameter tuning, experimenting with different parameter combinations to identify the configuration that yielded the best performance.

### Results

After manual hyperparameter tuning, the best Random Forest parameters were:

- n_estimators: 300
- max_depth: 10
- min_samples_split: 5
- min_samples_leaf: 2


The model achieved a Mean Absolute Error of 0.74, and an R² of 0.078, meaning it explains roughly 7–8% of the variance in DAYS_OUT_NEXT. This relatively low R² is expected because injury days are highly skewed and influenced by random events that are difficult to predict. Despite the low R², the model can still capture general trends and identify the most important features contributing to injury risk.\
\
Visualization of residuals and predictions helps assess where the model performs well and poorly.
<img width="679" height="696" alt="image" src="https://github.com/user-attachments/assets/234e3318-60fa-4193-95b6-ce2daad39daa" />
<img width="885" height="503" alt="image" src="https://github.com/user-attachments/assets/c3954f36-11ac-4eb9-a08c-8ffe0027b042" />

The Predicted vs Actual plot shows that the model captures general trends for players with low days out, but tends to underpredict rare longer injuries. Most predictions are clustered at the lower end due to the skewed distribution of DAYS_OUT_NEXT.
The residuals plot confirms this, residuals are small for the majority of players but increase for higher actual days out, indicating the model has difficulty predicting extreme injuries. Overall, the model is more reliable for predicting typical short-term injuries and highlights the challenge of predicting rare, high-impact injuries.

### How to Run
All modeling and results can be seen by running notebooks/modeling.ipynb. 


