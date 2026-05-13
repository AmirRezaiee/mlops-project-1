from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

def fetch():
    subprocess.run(["python", "/opt/airflow/scripts/fetch_data.py"])

def retrain():
    subprocess.run(["python", "/opt/airflow/scripts/retrain_model.py"])

with DAG(
    dag_id="ml_pipeline",
    start_date=datetime(2024,1,1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    t1 = PythonOperator(
        task_id="fetch_data",
        python_callable=fetch
    )

    t2 = PythonOperator(
        task_id="retrain_model",
        python_callable=retrain
    )

    t1 >> t2