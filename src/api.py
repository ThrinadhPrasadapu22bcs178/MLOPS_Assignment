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
try:
    mlruns_dir = os.path.join(os.path.dirname(__file__), '..', 'mlruns')
    mlflow.set_tracking_uri(f"file://{mlruns_dir}")
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
    if experiment:
        runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id], order_by=["start_time desc"], max_results=1)
        latest_run_id = runs.iloc[0].run_id
        model_uri = f"runs:/{latest_run_id}/model"
        model = mlflow.sklearn.load_model(model_uri)
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
    if not model:
        return {"error": "Model not loaded properly. Have you trained the model first?"}
        
    df = pd.DataFrame([request.features])
    prediction = model.predict(df)[0]
    
    return {
        "Prediction": int(prediction),
        "Name": STUDENT_NAME,
        "Roll Number": ROLL_NO
    }
