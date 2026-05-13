import os
import sqlite3
import numpy as np
import joblib
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression

# ------------------------
# MLflow config
# ------------------------
mlflow.set_tracking_uri("http://host.docker.internal:5000")
mlflow.set_experiment("ml_pipeline_experiment")

# ------------------------
# Paths
# ------------------------
MODEL_DIR = "/opt/airflow/models"
os.makedirs(MODEL_DIR, exist_ok=True)

DB_PATH = "/opt/airflow/pipeline.db"

# ------------------------
# Load Data
# ------------------------
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT prediction FROM pipeline_data")
rows = cursor.fetchall()

print("Rows:", len(rows))

if len(rows) < 5:
    print("Not enough data")
    exit()

y = np.array([r[0] for r in rows])
X = np.arange(len(y)).reshape(-1, 1)

# ------------------------
# Train + MLflow tracking
# ------------------------
with mlflow.start_run():

    model = LinearRegression()
    model.fit(X, y)

    preds = model.predict(X)
    mse = np.mean((y - preds) ** 2)

    # log params & metrics
    mlflow.log_param("model", "LinearRegression")
    mlflow.log_metric("mse", float(mse))

    # log model
    mlflow.sklearn.log_model(model, "model")

    # save locally too
    model_path = os.path.join(MODEL_DIR, "model.pkl")
    joblib.dump(model, model_path)

    print("Model saved at:", model_path)
    print("MSE:", mse)