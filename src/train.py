
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import os
import joblib

# 1. ساخت دیتای ساده
data = {
    "size": [50, 60, 80, 100, 120, 150, 200],
    "price": [150, 180, 240, 300, 360, 450, 600]
}

df = pd.DataFrame(data)

# 2. تقسیم داده
X = df[["size"]]
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 3. ساخت مدل
model = LinearRegression()
model.fit(X_train, y_train)

# 4. ارزیابی ساده
score = model.score(X_test, y_test)
print(f"Model Score: {score}")

# 5. ذخیره مدل
os.makedirs("../models", exist_ok=True)
joblib.dump(model, "../models/model.pkl")

print("Model saved in models/model.pkl")
