# Cloud-Computing-Coursework
COMM034 Coursework 2025

This coursework is divided into three main components:Task A (Text Analysis Cloud Application), Task B (BigQuery Jump Start + Looker studio + Cloud Run UI), and Task C (Video Demonstration).
Project Structure:
Task A

  task_a/text_analysis/analysis.py        # Text analysis functions (A1)

  task_a/functions/http_trigger/main.py   # HTTP Cloud Function (A2)

  task_a/functions/storage_trigger/main.py# Trigger when file is uploaded (A2/A3)

  task_a/functions/pubsub_worker/main.py  # Parallel processing worker (A3)

  task_a/functions/enqueue_http/main.py   # HTTP endpoint for enqueuing multiple files (A3)

  task_a/requirements.txt

Task B (BigQuery Jump Start + Looker Studio + Cloud Run)

  cloud_run_b5/app/app.py                 # Flask-based UI for query selection 

  cloud_run_b5/app/templates/index.html   # HTML template

  cloud_run_b5/Dockerfile

  cloud_run_b5/requirements.txt

  JUMPSTART_GUIDE.md                      # Guide for deploying the Jump Start Solution

sample_data/                               # Sample data files

run_local.py                                # Local testing for test analysis function

report/                                     # Draft versions of the report

DEPLOY_GCP.md                               # Complete GCP deployment commands
Quick Start: Deploy Jump Start Solution
For Task B4 (Looker Studio Dashboard):

Read JUMPSTART_GUIDE.md -which provides detailed instructions for deploying the Jump Start Solution.
Navigate to  https://console.cloud.google.com/solutions
Deploy "Data warehouse with BigQuery" solution.
Wait approximately 5-10 minutes, then open the automatically generated Looker Studio Dashboard.
Customise the dashboard according to the project requirements.

Benefits:

No need to manually create datasets (the solution uses the thelook_ecommerce dataset)
A pre-built Looker Studio dashboard is provided
Best practices from Google
Local Testing (Task A1)
To test the text analysis functionality locally, execute:
python run_local.py
Deploy Outline (GCP)
Enable the following APIs: Cloud Functions, Cloud Run, Pub/Sub, Artifact Registry, BigQuery
Create Storage buckets: input & output
Deploy http_trigger, storage_trigger, enqueue_http, pubsub_worker
Create a Pub/Sub topic & subscription for the worker
Upload files to the input bucket → storage trigger is activated → processing results are written to the output bucket.
Deploy Cloud Run (Task B5):
Create Artifact Registry repository
Build the container image and deploy it to Cloud Run.

Detailed deployment commands will be provided in the Deployment section of the final report.

