# ML Workflow with Airflow, FastAPI, and Streamlit

This repository contains an end-to-end machine learning workflow using Apache Airflow for orchestration, FastAPI for model predictions, and Streamlit for a user interface. The setup includes model training, evaluation, and deployment with AWS S3 for model storage and Redis for caching predictions.

## Table of Contents
- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Docker Compose Services](#docker-compose-services)
- [Accessing the Services](#accessing-the-services)
- [Contributing](#contributing)
- [License](#license)

## Overview

The project integrates several tools to create a robust machine learning pipeline:
- **Apache Airflow**: For orchestrating the ML workflow.
- **FastAPI**: For serving model predictions.
- **Streamlit**: For creating a user-friendly interface to input data and view predictions.
- **AWS S3**: For storing trained models and accuracy metrics.
- **Redis**: For caching predictions to improve performance.

## Directory Structure

```plaintext
my_project/
├── api/
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── streamlit_app.py
├── dags/
│   ├── __init__.py
│   ├── ml_workflow.py
│   ├── tasks/
│       ├── __init__.py
│       ├── process_data.py
│       ├── read_csv_from_s3.py
│       ├── save_model.py
│       └── train_and_evaluate.py
├── logs/
├── plugins/
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
