# Day 01: AI Fundamentals

## Project Overview
**Goal:** To build an end-to-end Machine Learning pipeline that predicts student performance based on study habits.
**Focus:** Data generation, cleaning, visualization, model training, and serialization (Pickling).

This project simulates a real-world backend AI workflow, moving from raw "dirty" data to a deployable model file.

## Tech Stack
* **Environment:** VS Code (Local `.venv` Kernel), Jupyter Notebook
* **Data Manipulation:** Pandas, NumPy
* **Visualization:** Matplotlib
* **Machine Learning:** Scikit-Learn (Linear Regression)
* **Serialization:** Joblib

## Key Achievements

### 1. Environment Setup
* Configured a professional local Data Science environment using `venv`.

### 2. Data Engineering
* **Synthetic Data Generation:** Created a dataset of 5,000 students using NumPy.
* **Data Cleaning:**
    * Identified and removed **50 duplicate rows**.
    * Detected **5% missing values** in `Study_Hours`.
    * Imputed missing values using the **Median** strategy to maintain statistical integrity.

### 3. Exploratory Data Analysis (EDA)
* Visualized the relationship between *Study Hours* and *Final Score*.
* Confirmed a strong positive linear correlation suitable for regression analysis.

### 4. Model Training & Evaluation
* **Algorithm:** Linear Regression
* **Split:** 80% Training / 20% Testing
* **Performance Metrics:**
    * **R² Score:** ~0.89 (Model explains 89% of the variance).
    * **MAE (Mean Absolute Error):** ~4.0 (Predictions are typically within +/- 4 points).

### 5. Deployment Preparation
* Serialized (saved) the trained model using `joblib` to `models/student_score_predictor.pkl`.
* Verified the saved model by reloading it and running a test prediction on new data.

## Project Structure
Week04_AI/
├── .venv/              # Local Python Environment (Hidden)
├── data/
│   └── student_performance.csv  # Raw/Cleaned Dataset
├── models/
│   └── student_score_predictor.pkl # Trained AI Model
├── notebooks/
│   └── Day01.ipynb     # Main Analysis Notebook
├── README.md           # Project Documentation
└── requirements.txt    # List of dependencies (pip freeze)