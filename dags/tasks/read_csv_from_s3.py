from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from io import StringIO
import pandas as pd

def read_csv_from_s3():
    s3_hook = S3Hook(aws_conn_id='aws_default')
    bucket_name = 'airflow-ml-orchestration'
    key = 'manufacturing_defect_dataset.csv'

    # Get the file content
    file_content = s3_hook.read_key(key, bucket_name)
    
    # Use StringIO to simulate a file object
    string_io_obj = StringIO(file_content)

    df = pd.read_csv(string_io_obj)
    print(df.head())

    return df.to_json()