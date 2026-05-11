from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, validator
import joblib
import numpy as np
import os
import sqlite3

app = FastAPI()

# ------------------------
# Load Model
# ------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "..", "models", "model.pkl")
model = joblib.load(model_path)

# ------------------------
# Database
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
# Input Model
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
    def validate_positive(cls, v):
        if v < 0:
            raise ValueError("Values must be positive")
        return v

# ------------------------
# Predict API
# ------------------------
@app.post("/predict")
def predict(data: InputData):
    features = np.array([[
        data.MedInc, data.HouseAge, data.AveRooms, data.AveBedrms,
        data.Population, data.AveOccup, data.Latitude, data.Longitude
    ]])

    pred = model.predict(features)[0]
    pred = max(0, pred)

    cursor.execute("""
    INSERT INTO predictions (
        MedInc, HouseAge, AveRooms, AveBedrms,
        Population, AveOccup, Latitude, Longitude, prediction
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.MedInc, data.HouseAge, data.AveRooms, data.AveBedrms,
        data.Population, data.AveOccup, data.Latitude, data.Longitude, pred
    ))
    conn.commit()

    return {"predicted_house_value": float(pred)}

# ------------------------
# History API
# ------------------------
@app.get("/history")
def get_history():
    cursor.execute("SELECT * FROM predictions ORDER BY id DESC LIMIT 20")
    rows = cursor.fetchall()

    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "prediction": r[9]
        })

    return data

# ------------------------
# UI + Dashboard
# ------------------------
@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
    <html>
    <head>
        <title>ML Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <style>
            body {
                background:#121212;
                color:white;
                font-family:Arial;
                display:flex;
                justify-content:center;
                align-items:center;
                height:100vh;
            }

            .card {
                width:700px;
                background:#1e1e1e;
                padding:20px;
                border-radius:10px;
            }

            input {
                margin:5px;
                padding:8px;
                background:#2c2c2c;
                color:white;
                border:none;
            }

            button {
                padding:10px;
                margin-top:10px;
                width:100%;
                background:green;
                color:white;
                border:none;
            }

            #result {
                margin-top:10px;
                text-align:center;
            }
        </style>
    </head>

    <body>
        <div class="card">
            <h2>🚀 ML Dashboard</h2>

            <input id="MedInc" placeholder="5.0">
            <input id="HouseAge" placeholder="20">
            <input id="AveRooms" placeholder="6">
            <input id="AveBedrms" placeholder="1">
            <input id="Population" placeholder="1000">
            <input id="AveOccup" placeholder="3">
            <input id="Latitude" placeholder="34.2">
            <input id="Longitude" placeholder="-118.4">

            <button onclick="predict()">Predict</button>

            <div id="result"></div>

            <canvas id="chart"></canvas>
        </div>

        <script>
        let chart;

        async function predict() {

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

            const res = await fetch("/predict", {
                method:"POST",
                headers:{"Content-Type":"application/json"},
                body:JSON.stringify(data)
            });

            const result = await res.json();
            document.getElementById("result").innerHTML =
                "💰 " + result.predicted_house_value;

            loadHistory();
        }

        async function loadHistory() {
            const res = await fetch("/history");
            const data = await res.json();

            const values = data.map(x => x.prediction);

            const ctx = document.getElementById("chart");

            if (chart) chart.destroy();

            chart = new Chart(ctx, {
                type:'line',
                data:{
                    labels: values.map((_,i)=>i+1),
                    datasets:[{
                        label:"Prediction History",
                        data:values,
                        borderColor:"green"
                    }]
                }
            });
        }

        loadHistory();
        </script>
    </body>
    </html>
    """