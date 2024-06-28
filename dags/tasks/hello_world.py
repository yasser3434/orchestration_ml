from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def hello_world():
    print("Hello, World!")

with DAG('hello_world_dag',
         start_date=datetime(2023, 1, 1),
         schedule_interval='@daily',
         catchup=False) as dag:

    hello_world_task = PythonOperator(
        task_id='hello_world',
        python_callable=hello_world
    )
