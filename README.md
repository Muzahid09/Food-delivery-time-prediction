## Food-delivery-time-prediction

This project is documented in a Medium blog series:
- **[Part 1: From Colab to a Reproducible Pipeline](https://medium.com/@muzahid023/mlops-part-1-from-colab-to-a-reproducible-pipeline-for-food-delivery-prediction-6abce16dd8b7)**: Focuses on experiment tracking, pipeline automation, and versioning.

  
==============================

## 📌Project Overview

This repository contains my implementation of a machine learning pipeline to predict food delivery times in minutes, built with an MLOps approach. The goal was to create a reliable, reproducible, and scalable workflow that transforms experimentation into a production-ready system.

![new_dvc](https://github.com/user-attachments/assets/7079bafe-6072-4862-b898-225189cb3a22)


## 🔄Workflow

## 🧪 1. Experimentation

- Initial experimentation was conducted using Google Colab.

- Logged experiments in MLflow, hosted remotely on DagsHub.

- Identified the best model through rigorous experimentation.

## 🏗 2. Building the DVC Pipeline

- Used VS Code for development.

- Constructed a DVC pipeline for data tracking and model training.

- Tracked data, models, and artifacts using DVC, storing them in AWS S3.

- Integrated MLflow tracking within the DVC pipeline.

- Registered the best model in the MLflow Model Registry using the pipeline.

## ⚡ 3. API Development & CI/CD

- Developed an API service using FastAPI to serve the model.

- Implemented GitHub Actions for CI/CD:

- Tested model loading and performance.

- Promoted the model to the production stage in the MLflow Model Registry if tests passed.

- Built a Docker image of the FastAPI app and pushed it to AWS ECR.

## ☁️ 4. Deployment

- Manually deployed the model using AWS Auto Scaling Group and Application Load Balancer.

- Explored Kubernetes deployment using Minikube.

## 🛠 Technologies Used

- Python (Data preprocessing, modeling, API development)

- Google Colab (Experimentation)

- MLflow (Experiment tracking, model registry)

- DVC (Data and pipeline versioning)

- AWS S3 (Data and model storage)

- FastAPI (API development)

- GitHub Actions (CI/CD)

- AWS ECR (Docker image storage)

- AWS Auto Scaling Group & Load Balancer (Model deployment)

- Minikube (Local Kubernetes deployment)


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
