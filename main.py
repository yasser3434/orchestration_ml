from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import json
import redis
from io import StringIO


app = FastAPI()

class InputData(BaseModel):
    ProductionVolume: int
    DefectRate: float
    QualityScore: float
    MaintenanceHours: int
    StockoutRate: float

def load_model(file_path):
    return joblib.load(file_path)


@app.get("/predict/")
async def predict(data: InputData):
    input_dict = {
        "Production Volume": data.ProductionVolume,
        "Defect Rate": data.DefectRate,
        "Quality Score": data.QualityScore,
        "Maintenance Hours": data.MaintenanceHours,
        "Stockout Rate": data.StockoutRate
    }


    input_df = pd.DataFrame([input_dict])
    model = load_model('model.pkl')
    prediction = model.predict(input_df)
    prediction = {"prediction": prediction[0][0]}
    return prediction