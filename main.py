from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib

app = FastAPI()

# Define a Pydantic model for the features
class PredictionRequest(BaseModel):
    ProductionVolume: int
    DefectRate: float
    QualityScore: float
    MaintenanceHours: int
    StockoutRate: float

# Load the trained model
model = joblib.load('model.pkl')

@app.post("/predict/")
async def predict(request: PredictionRequest):
    try:
        features = np.array([[
            request.ProductionVolume,
            request.DefectRate,
            request.QualityScore,
            request.MaintenanceHours,
            request.StockoutRate
        ]])
        
        prediction = model.predict(features)
        
        predicted_class = int(prediction[0] > 0.5) 
        
        return {"prediction": predicted_class}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
