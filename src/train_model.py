import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib
df = pd.read_csv("data/features_data.csv")

#features were gonna use (all of them to start) | Might want to take out position, and average days out last 3
features = [
    'AGE',
    'GAMES_PLAYED',
    'GAMES_STARTED',
    'MINUTES_PLAYED',
    'HEIGHT',
    'WEIGHT',
    'MPG',
    'injuries_last_3',
    'avg_days_out_last_3'
]

# one hot encoding for position
position_dummies = pd.get_dummies(df['POSITION'], prefix='POSITION')
df = pd.concat([df, position_dummies], axis=1)

# add position dummy columns to features
position_cols = [col for col in df.columns if col.startswith('POSITION_')]
features.extend(position_cols)

# prepare x and y
X = df[features].copy()
y = df['DAYS_OUT'].copy()

# handle missing values (should be none)
X.fillna(0, inplace=True)

# split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# random forest regression
print("Training Random Forest Regression model...")
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42
)

model.fit(X_train_scaled, y_train)

# make predictions | USE AS EXAMPLE IN NOTEBOOK
y_pred = model.predict(X_test_scaled)

# metrics
print("\n=== Model Performance ===")
print(f"Mean Absolute Error (MAE): {mean_absolute_error(y_test, y_pred):.2f} days")
print(f"Root Mean Squared Error (RMSE): {np.sqrt(mean_squared_error(y_test, y_pred)):.2f} days")
print(f"R² Score: {r2_score(y_test, y_pred):.4f}")

# stats
print("\n=== Prediction Statistics ===")
print(f"Average Actual Days Out: {y_test.mean():.2f} days")
print(f"Average Predicted Days Out: {y_pred.mean():.2f} days")
print(f"Std Dev of Predictions: {y_pred.std():.2f} days")
print(f"Min Prediction: {y_pred.min():.2f} days")
print(f"Max Prediction: {y_pred.max():.2f} days")

# feature importance
feature_importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n=== Feature Importance ===")
print(feature_importance)

# save for later (might want to pivot to something else after using notebooks)
joblib.dump(model, 'models/injury_risk_model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
joblib.dump(features, 'models/feature_names.pkl')

print("\nModel saved to 'models/injury_risk_model.pkl'")
print("Scaler saved to 'models/scaler.pkl'")
print("Feature names saved to 'models/feature_names.pkl'")

# example usage
def predict_days_out(player_data):
    """
    Predict days out for a player
    player_data: dict with feature values
    """
    # create df from input
    input_df = pd.DataFrame([player_data])
    
    # scale input
    input_scaled = scaler.transform(input_df[features])
    
    # predict
    predicted_days = model.predict(input_scaled)[0]
    
    # ensure positive prediction
    predicted_days = max(0, predicted_days)
    
    return {
        'predicted_days_out': round(predicted_days, 1),
        'risk_level': 'High' if predicted_days > 60 else 'Medium' if predicted_days > 30 else 'Low'
    }

# prediction on test set
sample_player = X_test.iloc[0].to_dict()
result = predict_days_out(sample_player)
actual_days = y_test.iloc[0]
print(f"\n=== Sample Prediction ===")
print(f"Predicted Days Out: {result['predicted_days_out']} days")
print(f"Actual Days Out: {actual_days} days")
print(f"Risk Level: {result['risk_level']}")