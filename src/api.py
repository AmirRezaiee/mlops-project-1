from fastapi import FastAPI
import joblib

# ساخت API
app = FastAPI()

# load مدل
model = joblib.load("../models/model.pkl")

# تست ساده
@app.get("/")
def home():
    return {"message": "ML Model API is running"}

# endpoint برای prediction
@app.get("/predict")
def predict(size: float):
    prediction = model.predict([[size]])
    return {
        "input_size": size,
        "predicted_price": float(prediction[0])
    }
