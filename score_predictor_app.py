import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Load your dataset
df = pd.read_csv("ODI_Match_Data.csv", low_memory=False)

# STEP 1: Feature Engineering
df['total_runs'] = df[['runs_off_bat', 'extras']].sum(axis=1)

# Convert ball to over (floor the decimal)
df['over'] = df['ball'].astype(str).str.extract(r'(\d+)\.(\d)').astype(float).apply(lambda x: x[0] + x[1]/6, axis=1)

# Group by match & innings to get cumulative scores
df = df.sort_values(by=['match_id', 'innings', 'ball'])
df['cumulative_runs'] = df.groupby(['match_id', 'innings'])['total_runs'].cumsum()
df['over_number'] = df['ball'].astype(str).str.extract(r'(\d+)\.').astype(float)

# Add key features
features_df = df.groupby(['match_id', 'innings', 'over_number']).agg({
    'cumulative_runs': 'last',
    'total_runs': 'sum',
    'player_dismissed': 'count'
}).reset_index()

features_df.rename(columns={
    'cumulative_runs': 'current_score',
    'player_dismissed': 'wickets_fallen',
    'over_number': 'overs_completed'
}, inplace=True)

# Add run rate in last 5 overs (moving window)
features_df['run_rate_last_5'] = features_df.groupby(['match_id', 'innings'])['current_score'].diff().rolling(5).mean() / 5
features_df['run_rate_last_5'] = features_df['run_rate_last_5'].fillna(method='bfill')

# Get final score per innings
final_scores = df.groupby(['match_id', 'innings'])['cumulative_runs'].max().reset_index()
final_scores.rename(columns={'cumulative_runs': 'final_score'}, inplace=True)

# Merge target
final_df = pd.merge(features_df, final_scores, on=['match_id', 'innings'], how='left')

# Rename for clarity
final_df['wickets_in_hand'] = 10 - final_df['wickets_fallen']

# Final feature set
model_features = ['current_score', 'wickets_in_hand', 'overs_completed', 'run_rate_last_5']
X = final_df[model_features].dropna()
y = final_df.loc[X.index, 'final_score']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = XGBRegressor(n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Predict & Evaluate
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("✅ Model Trained Successfully")
print("RMSE:", round(rmse, 2))
print("R² Score:", round(r2, 4))

# Save model for Streamlit
joblib.dump(model, "xgb_score_predictor.pkl")
