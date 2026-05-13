# 🏠 MLOps House Price Prediction

This project demonstrates an end-to-end Machine Learning system with both cloud deployment and local MLOps pipeline orchestration.

---

## 🚀 Live Demo

👉 https://mlops-project-1-3hei.onrender.com

Note:
- This live demo represents the deployed API and UI.
- The full MLOps pipeline (Airflow, MLflow, retraining) runs locally using Docker.

---

## 🧠 Features

### 🌐 Deployed (Cloud)
- FastAPI REST API
- Interactive web UI
- Model inference endpoint
- Hosted on Render

### ⚙️ MLOps Pipeline (Local)
- Airflow pipeline for data ingestion and retraining
- SQLite database for storing predictions
- Automated retraining workflow
- MLflow experiment tracking and model versioning
- Dockerized orchestration

---

## 🏗️ Project Structure

```bash
mlops-project-1/
│
├── src/
├── models/
├── dags/
├── scripts/
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## ⚙️ How It Works

### Cloud Flow
1. User submits input via UI
2. API processes request
3. Model returns prediction

### MLOps Flow (Local)
1. Airflow collects prediction data
2. Data stored in database
3. Model retrains automatically
4. MLflow logs experiments and models

---

## 🧪 Technologies Used

- Python
- FastAPI
- Scikit-learn
- Docker
- Airflow
- MLflow
- SQLite
- Render (Cloud)

---

## 📌 Key Highlight

This project separates:
- Real-time inference (cloud deployment)
- Model lifecycle management (local MLOps pipeline)

---

## 👨‍💻 Author

Amir Rezaei Darsara
