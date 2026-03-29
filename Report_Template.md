# MLOps Pipeline Implementation - Final Deliverable

## 1. Student Details
- **Name:** Thrinadh
- **Roll Number:** 2022BCS0178

## 2. Problem Description
- **Problem Statement:** Multiclass Classification of the Wine dataset. The objective is to correctly classify wines into one of three different cultivars based on their chemical properties.
- **Dataset Description:**
  - Source: sklearn wine dataset
  - Features: 13 numeric features (alcohol, malic acid, ash, etc.)
  - Target variable: 0, 1, 2 (representing 3 different classes of wine)
  - Dataset size: 178 instances (V1 uses 100 instances, V2 uses all 178)
  - Preprocessing steps: Loaded into Pandas DataFrame, Train/Test Split (80/20), optional Feature Selection (first 5 features).

## 3. Implementation Steps
- **DVC + S3 Setup:** Initialized DVC using `dvc init`. Configured AWS S3 bucket as remote using `dvc remote add`. Version 1 (100 rows) and Version 2 (178 rows) were added and tagged using Git, then pushed to S3.
- **CI/CD Pipeline:** Utilized GitHub Actions. The workflow `.github/workflows/mlops.yml` checks out the code, configures AWS credentials, pulls DVC data, trains the model, and uploads output metrics.
- **MLflow Integration:** Used MLflow tracking in `src/train.py`. Set experiment name to `2022BCS0178_experiment`. Logged parameters (model_type, n_estimators, feature_selection), metrics (accuracy, f1_score), and the model artifact.
- **API Implementation:** Created a FastAPI app in `src/api.py`. Implemented `/health` to return Name and Roll No. Implemented `/predict` to load the best local model from `mlruns/`, perform inference, and return the prediction along with Name and Roll No.
- **Dockerization:** Wrote a Dockerfile using python:3.9-slim, copying `src/` and `mlruns/` directories, installing requirements, and exposing port 8000 via Uvicorn. Built and pushed the image to Docker Hub as `thrinadhprasadapu/2022BCS0178-mlops`.

## 4. Experiment Results
### Table of 5 runs
| Run | Dataset | Model | Key Parameters | Metric 1 (Accuracy) | Metric 2 (F1 Score) |
|-----|---------|-------|----------------|---------------------|---------------------|
| 1   | V2      | RF    | n_est=100, fs=False| (Fill after running) | (Fill after running)|
| 2   | V2      | RF    | n_est=50, fs=False | (Fill after running) | (Fill after running)|
| 3   | V2      | RF    | n_est=100, fs=True | (Fill after running) | (Fill after running)|
| 4   | V2      | LR    | max_iter=1000  | (Fill after running) | (Fill after running)|
| 5   | V1      | RF    | n_est=100, fs=False| (Fill after running) | (Fill after running)|

### Comparison & Observations
- (Add your observations here comparing the metric changes when you adjusted hyperparameters, swapped datasets, or added feature selection)

## 5. Screenshots
*(Embed screenshots here to prove completion)*
1. **GitHub repository:** (Screenshot showing your repo `2022BCS0178-mlops-assignment`)
2. **DVC tracking and S3 bucket:** (Screenshot of terminal showing dvc push success, and AWS S3 bucket contents)
3. **CI/CD pipeline execution:** (Screenshot of GitHub Actions Success)
4. **MLflow runs (all 5):** (Screenshot of the MLflow UI showing 5 runs for `2022BCS0178_experiment`)
5. **Docker image in Docker Hub:** (Screenshot of Docker Hub repo `thrinadhprasadapu/2022BCS0178-mlops`)
6. **Running container:** (Screenshot of terminal `docker run` logs)
7. **API response with Name + Roll No:** (Screenshot of `http://localhost:8000/docs` executing `/predict` endpoint returning Thrinadh and 2022BCS0178)

## 6. Links
- **GitHub repository link:** https://github.com/your-username/2022BCS0178-mlops-assignment
- **Docker Hub link:** https://hub.docker.com/r/thrinadhprasadapu/2022BCS0178-mlops

## 7. Answers to Analysis Questions

### A. Run-Based Analysis
1. Which run performed the best? Why? *(Fill in your answer based on Table)*
2. How did dataset changes affect performance? *(V2 generally performs better due to having more data over V1)*
3. How did hyperparameter tuning affect results? *(Did changing n_estimators from 100 to 50 drop accuracy?)*
4. How did feature selection impact performance? *(Using top 5 features may reduce accuracy but improves inference speed)*
5. Which run performed worst? Explain why. *(Typically V1 or Feature Selected run due to lack of info/data)*
6. Which had greater impact: data change or parameter change? *(Answer based on your runs - usually data size has a bigger impact)*

### B. Experiment Tracking
1. How did MLflow help compare runs? *(It centralized metrics, parameters, and model artifacts without manual tracking)*
2. What information was most useful in selecting the best model? *(Accuracy and F1 Score logs mapped against the parameters in the MLflow UI)*

### C. Data Versioning
1. What differences were observed between dataset versions? *(V1 was partial with 100 rows, V2 was complete with 178 rows)*
2. Why is data versioning critical in ML systems? *(It ensures total reproducibility. Without knowing exactly what data a model trained on, reproducing results is impossible)*

### D. System Design
1. How does your pipeline ensure reproducibility? *(Using DVC for data tracking, Git for codebase versioning, AI model tracking with MLflow, and GitHub Actions for standardized execution)*
2. What are the limitations of your pipeline? *(Single static GitHub action without dynamic dataset ingestion, manual Docker commands instead of CI/CD docker image publisher)*
3. How would you improve this system for production use? *(Automate Docker image building and pushing via GitHub Actions, and deploy a Remote MLflow server instead of tracking locally)*
