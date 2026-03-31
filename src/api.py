from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
import os
import pandas as pd

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import STUDENT_NAME, ROLL_NO, EXPERIMENT_NAME

app = FastAPI()

# Load latest model locally from mlruns
import glob

try:
    mlruns_dir = os.path.join(os.path.dirname(__file__), '..', 'mlruns')
    model_path = None
    
    # Robustly search for the model.pkl file deeply
    for root, dirs, files in os.walk(mlruns_dir):
        if "model.pkl" in files:
            model_path = root
            break
            
    if model_path:
        model = mlflow.sklearn.load_model(model_path)
    else:
        model = None
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

class PredictRequest(BaseModel):
    features: list

@app.get("/")
@app.get("/health")
def health_check():
    return {
        "Name": STUDENT_NAME,
        "Roll No": ROLL_NO,
        "Status": "Healthy"
    }

@app.post("/predict")
def predict(request: PredictRequest):
    if model is None:
        return {"error": "Model not loaded properly. Have you trained it?"}
    try:
        df = pd.DataFrame([request.features])
        prediction = model.predict(df)[0]
        return {
            "Prediction": int(prediction),
            "Name": STUDENT_NAME,
            "Roll Number": ROLL_NO
        }
    except Exception as e:
        return {"error": str(e), "message": "Check feature count. Wine model needs 13 features."}
