import requests
import sqlite3

# API URL
API_URL = "http://host.docker.internal:8000/predict"

# sample data (همون که قبلاً داشتی)
data = {
    "MedInc": 5.0,
    "HouseAge": 20,
    "AveRooms": 6,
    "AveBedrms": 1,
    "Population": 1000,
    "AveOccup": 3,
    "Latitude": 34.2,
    "Longitude": 118.4
}

# ------------------------
# Call API
# ------------------------
response = requests.post(API_URL, json=data)

try:
    result = response.json()
except:
    raise Exception(f"Invalid JSON response: {response.text}")

# ------------------------
# DEBUG (خیلی مهم)
# ------------------------
print("API RESPONSE:", result)

# ------------------------
# Handle different response formats
# ------------------------
prediction = None

if "price" in result:
    prediction = result["price"]

elif "predicted_house_value" in result:
    prediction = result["predicted_house_value"]

else:
    raise Exception(f"Unexpected API response: {result}")

# ------------------------
# Save to DB
# ------------------------
conn = sqlite3.connect("/opt/airflow/pipeline.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pipeline_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction REAL
)
""")

cursor.execute(
    "INSERT INTO pipeline_data (prediction) VALUES (?)",
    (prediction,)
)

conn.commit()
conn.close()

print("Saved:", prediction)