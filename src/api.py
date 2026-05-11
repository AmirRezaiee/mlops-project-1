from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

model = joblib.load("models/model.pkl")


class InputData(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float


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


@app.get("/", response_class=HTMLResponse)
def form():
    return """
    <html>
    <head>
        <title>Price Predictor</title>

        <style>
            body {
                font-family: Arial;
                background: linear-gradient(135deg, #667eea, #764ba2);
                display: flex;
                justify-content: center;
                align-items: flex-start;
                min-height: 100vh;
                margin: 0;
                padding: 30px;
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

            input:focus {
                border-color: #667eea;
                outline: none;
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

            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
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

            .tooltip {
                font-size: 12px;
                color: #666;
                margin-bottom: 5px;
            }
        </style>
    </head>

    <body>
        <div class="card">
            <h2>🏠 Price Predictor</h2>

            <div class="tooltip">Median Income (higher = expensive area)</div>
            <input id="MedInc" placeholder="Median Income">

            <div class="tooltip">House Age (years)</div>
            <input id="HouseAge" placeholder="House Age">

            <div class="tooltip">Average number of rooms</div>
            <input id="AveRooms" placeholder="Average Rooms">

            <div class="tooltip">Average bedrooms</div>
            <input id="AveBedrms" placeholder="Bedrooms">

            <div class="tooltip">Population in area</div>
            <input id="Population" placeholder="Population">

            <div class="tooltip">Average occupancy</div>
            <input id="AveOccup" placeholder="Occupancy">

            <div class="tooltip">Latitude (location)</div>
            <input id="Latitude" placeholder="Latitude">

            <div class="tooltip">Longitude (location)</div>
            <input id="Longitude" placeholder="Longitude">

            <button onclick="predict()">Predict</button>

            <div id="result"></div>
        </div>

        <script>
        function formatCurrency(num) {
            return "$" + num.toLocaleString(undefined, {minimumFractionDigits: 2});
        }

        async function predict() {
            const resultDiv = document.getElementById("result");

            resultDiv.innerHTML = "<div class='spinner'></div>";
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

                for (let key in data) {
                    if (isNaN(data[key])) {
                        throw new Error("All fields must be numbers");
                    }
                    if (data[key] < 0) {
                        throw new Error("Values must be positive");
                    }
                }

                const response = await fetch("/predict", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                resultDiv.innerHTML = "💰 Price: " + formatCurrency(result.predicted_house_value);
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