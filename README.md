# MLOps Pipeline Assignment

## Step 1: Initialize Git and DVC
1. Open a terminal in this project folder (`d:\MLOPS_Assignment`).
2. Run `git init`
3. Run `dvc init`
4. Setup S3 (Replace `<your-bucket-name>` once you create it): 
   `dvc remote add -d myremote s3://<your-bucket-name>/mlops`

## Step 2: Data Versioning (v1 and v2)
1. Set up a virtual env and install requirements: `pip install -r requirements.txt`
2. Generate v1 dataset (partial - 100 rows): `python src/data_gen.py v1`
3. Track it with DVC: `dvc add data/dataset.csv`
4. Commit to Git: 
   `git add data/dataset.csv.dvc .gitignore` 
   `git commit -m "add dataset v1"`
5. Tag it: `git tag -a "v1" -m "version 1"`
6. Generate v2 dataset (full - 178 rows): `python src/data_gen.py v2`
7. Track it with DVC: `dvc add data/dataset.csv`
8. Commit to Git: 
   `git add data/dataset.csv.dvc` 
   `git commit -m "add dataset v2"`
9. Tag it: `git tag -a "v2" -m "version 2"`
10. Push data to S3: `dvc push`

## Step 3: MLflow Tracking (5 Runs)
You must perform 5 runs. The script `src/train.py` handles the logging automatically. 
Run the following commands locally:

**Run 1 (Dataset v2 - Base):**
`python src/train.py --model_type rf`

**Run 2 (Dataset v2 - Hyperparameter Change):**
`python src/train.py --model_type rf --n_estimators 50`

**Run 3 (Dataset v2 - Feature Selection):**
`python src/train.py --model_type rf --feature_selection`

**Run 4 (Dataset v2 - Different Model):**
`python src/train.py --model_type lr`

**Run 5 (Dataset v1 - Earlier Dataset):**
1. Checkout v1: `git checkout v1`
2. Pull old data: `dvc pull`
3. Train: `python src/train.py --model_type rf`
4. Restore latest: `git checkout main` and `dvc pull`

Run `mlflow ui` to view the 5 runs and take your screenshots.

## Step 4: Test API
1. Start the FastAPI server locally to verify: `uvicorn src.api:app --reload`
2. Navigate to `http://127.0.0.1:8000/docs` to test the endpoints and verify your Name and Roll Number appear in the output.

## Step 5: Dockerization
1. Ensure your `mlruns/` and `metrics.json` are present in the directory.
2. Build the Docker image: `docker build -t thrinadhprasadapu/2022BCS0178-mlops .`
3. Push to Docker Hub: `docker push thrinadhprasadapu/2022BCS0178-mlops`
4. Test running the container locally (Inference Validation): 
   `docker run -p 8000:8000 thrinadhprasadapu/2022BCS0178-mlops`

## Step 6: CI/CD Pipeline
1. Create a repository on GitHub named `2022BCS0178-mlops-assignment`.
2. Add your AWS credentials to GitHub Repository Secrets (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`).
3. Add remote and push:
   `git remote add origin https://github.com/your-github-username/2022BCS0178-mlops-assignment.git`
   `git push -u origin main`
4. The GitHub Action will automatically run and upload your `metrics.json` artifact!
