from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from tasks.read_csv_from_s3 import read_csv_from_s3
from tasks.process_data import process_data
from tasks.train_and_evaluate import train_and_evaluate
from tasks.save_model import save_model_to_s3

with DAG('ml_workflow', start_date=datetime(2023, 1, 1), schedule_interval='@daily', catchup=False) as dag:

    read_csv_task = PythonOperator(
        task_id='read_csv_from_s3',
        python_callable=read_csv_from_s3
    )

    # process_data_task = PythonOperator(
    #     task_id='process_data',
    #     python_callable=process_data,
    #     op_args=[read_csv_task.output]
    # )

    train_evaluate_task = PythonOperator(
        task_id='train_and_evaluate',
        python_callable=train_and_evaluate,
        op_args=[read_csv_task.output]
    )

    save_model_task = PythonOperator(
        task_id='save_model_to_s3',
        python_callable=save_model_to_s3,
        op_args=[
            train_evaluate_task.output,
            'model',  # Base name for the model file
            'airflow-ml-models'  # S3 bucket name
        ]
    )

    read_csv_task >> train_evaluate_task >> save_model_task
