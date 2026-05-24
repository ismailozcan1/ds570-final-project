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

```text
data/raw/steam-200k.csv
```

## Current Project Structure

```text
ds570-final-project/
├── data/
│   ├── raw/
│   │   └── steam-200k.csv
│   └── processed/
│       └── user_features.csv
├── notebooks/
│   ├── 01_data_loading_and_eda.ipynb
│   ├── 02_feature_engineering_and_clustering.ipynb
│   └── 03_modeling_and_evaluation.ipynb
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_processing.py
│   ├── clustering.py
│   ├── modeling.py
│   └── visualization.py
├── outputs/
│   ├── figures/
│   ├── reports/
│   └── models/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Current Progress

So far, the project includes:

- Initial project folder structure
- Raw Steam dataset
- Data loading functions
- Basic cleaning functions
- User-level feature engineering
- Processed user feature table
- Exploratory data analysis notebook
- Feature engineering and clustering notebook
- Predictive modeling and evaluation notebook

The raw interaction-level data is converted into user-level features such as:

- total_hours
- avg_hours
- max_hours
- unique_games
- purchase_count
- total_interactions
- hours_per_game
- purchase_ratio

These features are used for EDA, clustering, PCA visualization, predictive modeling, and dashboard development.

## Planned Next Steps

The next parts of the project will include:

1. Association rule analysis
2. Recommendation-oriented insights
3. Streamlit dashboard improvements
4. Docker testing
5. Final README updates

## Docker Usage

The project includes a Dockerfile. The Streamlit dashboard will be run with Docker.

Build the Docker image:

```bash
docker build -t ds570-steam-project .
```

Run the container:

```bash
docker run -p 8501:8501 ds570-steam-project
```

Then open the dashboard at:

```text
http://localhost:8501
```
