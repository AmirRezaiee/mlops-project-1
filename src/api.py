from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# load model
model = joblib.load("models/model.pkl")


# =========================
# API Input (JSON)
# =========================
class InputData(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float


# =========================
# API Endpoint
# =========================

    prediction = model.predict(features)[0]

    # جلوگیری از مقدار منفی
    prediction = max(0, prediction)

    return {
        "predicted_house_value": float(prediction)
    }


# =========================
# UI Level 2 (Frontend)
# =========================
@app.get("/", response_class=HTMLResponse)
def form():
    return """
    <html>
    <head>
        <title>House Price Predictor</title>

        <style>
            body {
                font-family: Arial;
                background: linear-gradient(135deg, #667eea, #764ba2);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }

            .card {
                background: white;
                padding: 30px;
                border-radius: 12px;
                width: 360px;
                box-shadow: 0px 10px 30px rgba(0,0,0,0.25);
            }

            h2 {
                text-align: center;
                margin-bottom: 20px;
            }

            input {
                width: 100%;
                padding: 10px;
                margin: 6px 0;
                border-radius: 6px;
                border: 1px solid #ccc;
            }

            button {
                width: 100%;
                padding: 12px;
                margin-top: 10px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
            }

            button:hover {
                background: #5a67d8;
            }

            #result {
                margin-top: 15px;
                padding: 10px;
                text-align: center;
                font-weight: bold;
                border-radius: 6px;
            }

            .success {
                background: #d4edda;
                color: #155724;
            }

            .error {
                background: #f8d7da;
                color: #721c24;
            }
        </style>
    </head>

    <body>
        <div class="card">
            <h2>🏠 Price Predictor</h2>

            <input id="MedInc" placeholder="Median Income">
            <input id="HouseAge" placeholder="House Age">
            <input id="AveRooms" placeholder="Average Rooms">
            <input id="AveBedrms" placeholder="Bedrooms">
            <input id="Population" placeholder="Population">
            <input id="AveOccup" placeholder="Occupancy">
            <input id="Latitude" placeholder="Latitude">
            <input id="Longitude" placeholder="Longitude">

            <button onclick="predict()">Predict</button>

            <div id="result"></div>
        </div>

        <script>
        async function predict() {
            const resultDiv = document.getElementById("result");

            resultDiv.innerHTML = "⏳ Predicting...";
            resultDiv.className = "";

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

                // validation
                for (let key in data) {
                    if (isNaN(data[key])) {
                        throw new Error("Please enter valid numbers in all fields");
                    }
                }

                const response = await fetch("/predict", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                resultDiv.innerHTML = "💰 Price: " + result.predicted_house_value.toFixed(2);
                resultDiv.className = "success";

            } catch (err) {
                resultDiv.innerHTML = "❌ " + err.message;
                resultDiv.className = "error";
            }
        }
        </script>

    </body>
    </html>
    """