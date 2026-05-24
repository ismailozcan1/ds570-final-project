# DS570 Final Project

## Explainable Steam User Segmentation and Game Recommendation Dashboard

This repository contains my final project for the DS570 Practical Applications of Data Science course.

The project focuses on Steam user behavior. I use the Steam-200k dataset to analyze how users purchase and play games. The main idea is to transform the raw user-game interaction data into user-level behavioral features, then use these features for exploratory analysis, clustering, model evaluation, and an interactive Streamlit dashboard.

## Dataset

The dataset used in this project is the Steam Video Games dataset from Kaggle:

https://www.kaggle.com/datasets/tamber/steam-video-games

The raw data contains user-game interactions. Each row includes a user id, game title, action type, and value.

The action column mainly includes:

- purchase
- play

For purchase rows, the value is recorded as 1.0. Since this does not represent real playtime, purchase actions are handled separately during feature engineering.

The raw dataset is stored in:

data/raw/steam-200k.csv

## Current Project Structure

ds570-final-project/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
├── outputs/
├── app.py
├── requirements.txt
├── Dockerfile
└── README.md

## Current Progress

So far, the project includes:

- Initial project folder structure
- Raw Steam dataset
- Data loading functions
- Basic cleaning functions
- User-level feature engineering
- Processed user feature table

The raw interaction-level data is converted into user-level features such as:

- total_hours
- avg_hours
- max_hours
- unique_games
- purchase_count
- total_interactions
- hours_per_game
- purchase_ratio

These features will be used in the next steps for EDA, clustering, PCA visualization, predictive modeling, and dashboard development.

## Planned Next Steps

The next parts of the project will include:

1. Exploratory data analysis
2. User behavior visualizations
3. K-Means clustering
4. Elbow Method and Silhouette Score
5. PCA visualization
6. Predictive model comparison
7. Decision Tree interpretation
8. Streamlit dashboard
9. Docker testing

## Docker Usage

The project includes a Dockerfile. The Streamlit dashboard will be run with Docker.

Build the Docker image:

docker build -t ds570-steam-project .

Run the container:

docker run -p 8501:8501 ds570-steam-project

Then open the dashboard at:

http://localhost:8501
