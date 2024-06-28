import joblib
from io import BytesIO
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime
import base64

def save_model_to_s3(model_base64, base_filename, bucket_name):
    
    # Decode the base64 encoded model
    model_data = base64.b64decode(model_base64)
    model_buffer = BytesIO(model_data)
    model = joblib.load(model_buffer)
    
    # Current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    model_filename = f"{base_filename}-{timestamp}.pkl"
    accuracy_filename = f"accuracy-{timestamp}.json"

    # Serialize model into a bytes buffer
    buffer = BytesIO()
    joblib.dump(model, buffer)
    buffer.seek(0)

    # Initialize the S3 Hook
    s3_hook = S3Hook()

    # Save the model to an S3 bucket
    s3_hook.load_bytes(
        buffer.getvalue(),
        bucket_name=bucket_name,
        key=model_filename,
        replace=True  # Overwrite if the file already exists
    )
    print(f"Model saved to S3 bucket {bucket_name} with filename {model_filename}")