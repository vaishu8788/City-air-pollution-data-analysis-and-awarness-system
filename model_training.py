import pandas as pd
from sklearn.ensemble import RandomForestRegressor  # or Classifier if you classify
from sklearn.model_selection import train_test_split
import pickle

# Load CSV
data = pd.read_csv("pollution1.csv")
print(data.columns.tolist())

# Replace with your actual column names
X = data[['SO2', 'CO2', 'PM10', 'PM2.5', 'Temperature (°C)']]
y = data['AQI']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Save model
with open('pollution_predictor.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model trained and saved successfully!")
