# ML Workflow with Airflow, FastAPI, and Streamlit

This repository contains an end-to-end machine learning workflow using Apache Airflow for orchestration, FastAPI for model predictions, and Streamlit for a user interface. The setup includes model training, evaluation, and deployment with AWS S3 for model storage and Redis for caching predictions.

## Overview

The project integrates several tools to create a robust machine learning pipeline:
- **Apache Airflow**: For orchestrating the ML workflow.
- **FastAPI**: For serving model predictions.
- **Streamlit**: For creating a user-friendly interface to input data and view predictions.
- **AWS S3**: For storing trained models and accuracy metrics.
- **Redis**: For caching predictions to improve performance.
