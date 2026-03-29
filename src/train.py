import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
import mlflow
import json
import argparse
import os

# Ensure the script can be run from root or src/
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import STUDENT_NAME, ROLL_NO, EXPERIMENT_NAME

def train(model_type='rf', n_estimators=100, feature_selection=False):
    df_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'dataset.csv')
    df = pd.read_csv(df_path)
    
    # Feature Selection (use only top 5 features vs all)
    all_features = df.columns.drop('target').tolist()
    if feature_selection:
        features = all_features[:5]
    else:
        features = all_features
        
    X = df[features]
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    mlflow.set_experiment(EXPERIMENT_NAME)
    with mlflow.start_run():
        if model_type == 'rf':
            model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
        else:
            model = LogisticRegression(max_iter=1000, random_state=42)
            
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        
        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds, average='weighted')
        
        mlflow.log_param("model_type", model_type)
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("feature_selection", feature_selection)
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)
        mlflow.sklearn.log_model(model, "model")
        
        print(f"Run completed. Acc: {acc:.4f}, F1: {f1:.4f}")
        
        # Save output metrics JSON (Mandatory Identification)
        metrics_output = {
            "Student Name": STUDENT_NAME,
            "Roll No": ROLL_NO,
            "accuracy": acc,
            "f1_score": f1
        }
        
        out_path = os.path.join(os.path.dirname(__file__), '..', 'metrics.json')
        with open(out_path, 'w') as f:
            json.dump(metrics_output, f, indent=4)
        print(f"Metrics saved to {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_type', type=str, default='rf', choices=['rf', 'lr'])
    parser.add_argument('--n_estimators', type=int, default=100)
    parser.add_argument('--feature_selection', action='store_true')
    args = parser.parse_args()
    
    train(args.model_type, args.n_estimators, args.feature_selection)
