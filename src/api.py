from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# load model
model = joblib.load("models/model.pkl")


# =========================
# JSON Input (API)
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
# UI (HTML Form)
# =========================
@app.get("/", response_class=HTMLResponse)
def form():
    return """
    <html>
    <head>
        <title>House Price Prediction</title>
        <style>
            body {
                font-family: Arial;
                background-color: #f4f6f8;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }

            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0px 0px 15px rgba(0,0,0,0.1);
                width: 350px;
            }

            h2 {
                text-align: center;
                margin-bottom: 20px;
            }

            input {
                width: 100%;
                padding: 8px;
                margin: 5px 0 15px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }

            button {
                width: 100%;
                padding: 10px;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }

            button:hover {
                background-color: #0056b3;
            }

            .result {
                margin-top: 20px;
                padding: 10px;
                background-color: #e6f7ff;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h2>House Price Prediction</h2>

            <form action="/predict-form" method="post">
                <input type="text" name="MedInc" placeholder="Median Income">
                <input type="text" name="HouseAge" placeholder="House Age">
                <input type="text" name="AveRooms" placeholder="Average Rooms">
                <input type="text" name="AveBedrms" placeholder="Average Bedrooms">
                <input type="text" name="Population" placeholder="Population">
                <input type="text" name="AveOccup" placeholder="Average Occupancy">
                <input type="text" name="Latitude" placeholder="Latitude">
                <input type="text" name="Longitude" placeholder="Longitude">

                <button type="submit">Predict</button>
            </form>
        </div>
    </body>
    </html>
    """


# =========================
# API (JSON)
# =========================
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

    # جلوگیری از منفی
    prediction = max(0, prediction)

    return {
        "predicted_house_value": float(prediction)
    }


# =========================
# Form Handler (UI)
# =========================
@app.post("/predict-form", response_class=HTMLResponse)
def predict_form(
    MedInc: float = Form(...),
    HouseAge: float = Form(...),
    AveRooms: float = Form(...),
    AveBedrms: float = Form(...),
    Population: float = Form(...),
    AveOccup: float = Form(...),
    Latitude: float = Form(...),
    Longitude: float = Form(...)
):
    features = np.array([[MedInc, HouseAge, AveRooms, AveBedrms,
                          Population, AveOccup, Latitude, Longitude]])

    prediction = model.predict(features)[0]

    # جلوگیری از منفی
    prediction = max(0, prediction)

    return f"""
    <html>
    <body style="font-family: Arial; background:#f4f6f8; display:flex; justify-content:center; align-items:center; height:100vh;">
        <div style="background:white; padding:30px; border-radius:10px; box-shadow:0px 0px 15px rgba(0,0,0,0.1); text-align:center;">
            <h2>Prediction Result</h2>
            <p style="font-size:18px;">Predicted House Value:</p>
            <p style="font-size:24px; color:#007BFF;">{prediction}</p>
            <br>
            <a href="/" style="text-decoration:none; color:white; background:#007BFF; padding:10px 20px; border-radius:5px;">Back</a>
        </div>
    </body>
    </html>
    """