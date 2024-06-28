from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import aioredis
from typing import List
import json
import boto3
from datetime import datetime
from io import BytesIO

# Initialize FastAPI app
app = FastAPI()

# Initialize Redis client
redis = aioredis.from_url("redis://redis")

# S3 Configuration
S3_BUCKET_NAME = "airflow-ml-models"
S3_MODEL_PREFIX = "model"

s3_client = boto3.client('s3')

# Function to fetch the latest model from S3
def fetch_latest_model_from_s3():
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=S3_MODEL_PREFIX)
    
    if 'Contents' not in response:
        raise Exception("No models found in S3 bucket.")
    
    # Find the latest model based on the timestamp in the filename
    latest_model = max(response['Contents'], key=lambda x: x['LastModified'])
    model_key = latest_model['Key']

    # Download the latest model
    model_obj = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=model_key)
    model_data = model_obj['Body'].read()
    
    # Deserialize the model
    model = joblib.load(BytesIO(model_data))
    return model

# Load the model during startup
@app.on_event("startup")
async def startup_event():
    global model
    model = fetch_latest_model_from_s3()
    await redis.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    await redis.close()

# Define the request model
class PredictionRequest(BaseModel):
    ProductionVolume: int
    DefectRate: float
    QualityScore: float
    MaintenanceHours: int
    StockoutRate: float

# Define the response model
class PredictionResponse(BaseModel):
    prediction: int

# Utility function to generate a Redis key
def generate_cache_key(data: dict) -> str:
    return "prediction:" + ":".join(f"{key}={value}" for key, value in data.items())

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    data = request.dict()
    cache_key = generate_cache_key(data)

    # Check the cache
    cached_prediction = await redis.get(cache_key)
    if cached_prediction:
        prediction = int(cached_prediction)
    else:
        # If not cached, perform the prediction
        df = pd.DataFrame([data])
        prediction = model.predict(df)[0]

        # Cache the prediction
        await redis.set(cache_key, str(prediction))

    return PredictionResponse(prediction=prediction)

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
