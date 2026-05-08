import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import fetch_california_housing
import joblib
import os
import mlflow
import mlflow.sklearn

mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("housing-price-prediction")

mlflow.start_run()

# load dataset
data = fetch_california_housing(as_frame=True)
df = data.frame

X = df.drop("MedHouseVal", axis=1)
y = df["MedHouseVal"]

# split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# model (upgrade)
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

# evaluation
score = model.score(X_test, y_test)
print(f"Model Score: {score}")

mlflow.log_metric("r2_score", score)

# save
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/model.pkl")

mlflow.sklearn.log_model(model, "model")

mlflow.end_run()

print("Model upgraded and saved")