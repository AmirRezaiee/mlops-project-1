from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI()

# ------------------------
# FIX PATH برای Render
# ------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "..", "models", "model.pkl")

model = joblib.load(model_path)


# ------------------------
# API Input
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

    return {"predicted_house_value": float(prediction)}


# ------------------------
# UI (Dark + Chart + UX Fix)
# ------------------------
@app.get("/", response_class=HTMLResponse)
def form():
    return """
    <html>
    <head>
        <title>Price Predictor</title>

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <style>
            body {
                font-family: Arial;
                background: #121212;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }

            .card {
                background: #1e1e1e;
                padding: 25px;
                border-radius: 12px;
                width: 650px;
                box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
            }

            h2 {
                text-align: center;
            }

            .grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-top: 10px;
            }

            input {
                padding: 10px;
                border-radius: 6px;
                border: none;
                background: #2c2c2c;
                color: white;
            }

            button {
                width: 100%;
                padding: 12px;
                margin-top: 15px;
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
            }

            #result {
                margin-top: 15px;
                text-align: center;
                font-weight: bold;
            }

            .spinner {
                border: 4px solid #333;
                border-top: 4px solid #4CAF50;
                border-radius: 50%;
                width: 20px;
                height: 20px;
                animation: spin 1s linear infinite;
                margin: auto;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>

    <body>
        <div class="card">
            <h2>🌙 Price Predictor</h2>

            <div class="grid">
                <input id="MedInc" placeholder="e.g. 5.0">
                <input id="HouseAge" placeholder="e.g. 20">
                <input id="AveRooms" placeholder="e.g. 6">
                <input id="AveBedrms" placeholder="e.g. 1">
                <input id="Population" placeholder="e.g. 1000">
                <input id="AveOccup" placeholder="e.g. 3">
                <input id="Latitude" placeholder="e.g. 34.2">
                <input id="Longitude" placeholder="e.g. -118.4">
            </div>

            <button onclick="predict()">Predict</button>

            <div id="result"></div>

            <canvas id="chart"></canvas>
        </div>

        <script>
        let chart;

        function formatCurrency(num) {
            return "$" + num.toLocaleString(undefined, {minimumFractionDigits: 2});
        }

        async function predict() {
            const resultDiv = document.getElementById("result");
            resultDiv.innerHTML = "<div class='spinner'></div>";

            try {
                const data = {
                    MedInc: parseFloat(document.getElementById("MedInc").value),
                    HouseAge: parseFloat(document.getElementById("HouseAge").value),
                    AveRooms: parseFloat(document.getElementById("AveRooms").value),
                    AveBedrms: parseFloat(document.getElementById("AveBedrms").value),
                    Population: parseFloat(document.getElementById("Population").value),
                    AveOccup: parseFloat(document.getElementById("AveOccup").value),
                    Latitude: parseFloat(document.getElementById("Latitude").value),
                    Longitude: parseFloat(document.getElementById("Longitude").value)
                };

                for (let key in data) {
                    if (isNaN(data[key])) {
                        throw new Error("All fields must be numbers");
                    }
                }

                const response = await fetch("/predict", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(data)
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error("API Error: " + errorText);
                }

                const result = await response.json();

                resultDiv.innerHTML = "💰 " + formatCurrency(result.predicted_house_value);

                const ctx = document.getElementById("chart").getContext("2d");

                if (chart) chart.destroy();

                chart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ["Prediction"],
                        datasets: [{
                            label: "House Price",
                            data: [result.predicted_house_value],
                            backgroundColor: "#4CAF50"
                        }]
                    }
                });

            } catch (err) {
                resultDiv.innerHTML = "❌ " + err.message;
            }
        }
        </script>
    </body>
    </html>
    """