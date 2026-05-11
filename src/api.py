from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, validator
import joblib
import numpy as np
import os
import sqlite3

app = FastAPI()

# ------------------------
# Load Model (Fix for Render)
# ------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "..", "models", "model.pkl")
model = joblib.load(model_path)

# ------------------------
# Database Setup
# ------------------------
DB_PATH = os.path.join(BASE_DIR, "..", "predictions.db")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    MedInc REAL,
    HouseAge REAL,
    AveRooms REAL,
    AveBedrms REAL,
    Population REAL,
    AveOccup REAL,
    Latitude REAL,
    Longitude REAL,
    prediction REAL
)
""")
conn.commit()

# ------------------------
# Input Validation
# ------------------------
class InputData(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float

    @validator('*')
    def check_positive(cls, v):
        if v < 0:
            raise ValueError("All values must be positive")
        return v

# ------------------------
# API Endpoint
# ------------------------
@app.post("/predict")
def predict_api(data: InputData):

    features = np.array([[
        data.MedInc,
        data.HouseAge,
        data.AveRooms,
        data.AveBedrms,
        data.Population,
        data.AveOccup,
        data.Latitude,
        data.Longitude
    ]])

    prediction = model.predict(features)[0]
    prediction = max(0, prediction)

    # Save to DB
    cursor.execute("""
    INSERT INTO predictions (
        MedInc, HouseAge, AveRooms, AveBedrms,
        Population, AveOccup, Latitude, Longitude, prediction
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.MedInc, data.HouseAge, data.AveRooms, data.AveBedrms,
        data.Population, data.AveOccup, data.Latitude, data.Longitude,
        prediction
    ))

    conn.commit()

    return {"predicted_house_value": float(prediction)}

# ------------------------
# UI (Dark + Chart + Validation)
# ------------------------
@app.get("/", response_class=HTMLResponse)
def form():
    return """
    <html>
    <head>
        <title>ML App</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <style>
            body {
                background: #121212;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                font-family: Arial;
            }

            .card {
                background: #1e1e1e;
                padding: 25px;
                border-radius: 12px;
                width: 650px;
            }

            .grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
            }

            input {
                padding: 10px;
                background: #2c2c2c;
                border: none;
                color: white;
            }

            button {
                margin-top: 15px;
                padding: 12px;
                width: 100%;
                background: green;
                color: white;
                border: none;
            }

            #result {
                margin-top: 15px;
                text-align: center;
            }
        </style>
    </head>

    <body>
        <div class="card">
            <h2>🌙 ML Predictor</h2>

            <div class="grid">
                <input id="MedInc" placeholder="5.0">
                <input id="HouseAge" placeholder="20">
                <input id="AveRooms" placeholder="6">
                <input id="AveBedrms" placeholder="1">
                <input id="Population" placeholder="1000">
                <input id="AveOccup" placeholder="3">
                <input id="Latitude" placeholder="34.2">
                <input id="Longitude" placeholder="-118.4">
            </div>

            <button onclick="predict()">Predict</button>

            <div id="result"></div>
            <canvas id="chart"></canvas>
        </div>

        <script>
        let chart;

        function formatCurrency(num) {
            return "$" + num.toLocaleString();
        }

        async function predict() {

            const resultDiv = document.getElementById("result");

            const data = {
                MedInc: parseFloat(MedInc.value),
                HouseAge: parseFloat(HouseAge.value),
                AveRooms: parseFloat(AveRooms.value),
                AveBedrms: parseFloat(AveBedrms.value),
                Population: parseFloat(Population.value),
                AveOccup: parseFloat(AveOccup.value),
                Latitude: parseFloat(Latitude.value),
                Longitude: parseFloat(Longitude.value)
            };

            for (let key in data) {
                if (isNaN(data[key])) {
                    resultDiv.innerHTML = "❌ Invalid input";
                    return;
                }
            }

            try {
                const response = await fetch("/predict", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                resultDiv.innerHTML = "💰 " + formatCurrency(result.predicted_house_value);

                const ctx = document.getElementById("chart");

                if (chart) chart.destroy();

                chart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ["Prediction"],
                        datasets: [{
                            label: "Price",
                            data: [result.predicted_house_value],
                            backgroundColor: "green"
                        }]
                    }
                });

            } catch (err) {
                resultDiv.innerHTML = "❌ API Error";
            }
        }
        </script>
    </body>
    </html>
    """