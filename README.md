# Explainable Steam User Segmentation Dashboard

This repository contains my final project for the DS570 Practical Applications of Data Science course.

The project analyzes Steam users' purchasing and gameplay behavior using the Steam-200k dataset. The main idea is to start from raw user-game interaction data, create user-level behavioral features, discover user segments with K-Means clustering, and then explain these segments with supervised machine learning models and Decision Tree interpretability.

The project is not only a notebook-based analysis. It also includes a Streamlit dashboard and Docker configuration so that the results can be explored as an interactive application.

---

## Project Objective

The original dataset is interaction-level data. Each row shows whether a user purchased or played a specific game. This format is useful, but it does not directly tell us what type of Steam user someone is.

In this project, I transform the raw interaction data into user-level behavioral profiles and try to answer the following question:

**Can Steam users be grouped into meaningful and explainable behavior segments based on their purchasing behavior, game diversity, and playtime intensity?**

The important point is that Steam user behavior should not be explained only by total playtime. A user who buys many games but plays very little is different from a user who owns fewer games but spends many hours on them. Because of this, I used multiple behavioral features instead of relying on only one variable.

---

## Dataset

The dataset used in this project is the Steam Video Games dataset from Kaggle:

[https://www.kaggle.com/datasets/tamber/steam-video-games](https://www.kaggle.com/datasets/tamber/steam-video-games)

The raw data contains Steam user-game interactions with the following structure:

```text
user_id | game | action | value
```

The `action` column mainly contains two values:

* `purchase`
* `play`

A key detail in this dataset is that purchase rows have a value of `1.0`. This value does not mean one hour of playtime. It only means that the user purchased the game. Because of this, purchase rows are not treated as playtime. Instead, purchasing behavior is handled separately during feature engineering.

The raw dataset is stored in `data/raw/steam-200k.csv`.

The processed files used by the dashboard are stored in `data/processed/`.

The dataset is included in the repository because it is public and small enough for this project. This also allows the Docker container to run without asking the user to download data manually or log in to an external service.

---

## Repository Structure

```text
steam-user-segmentation-dashboard/
├── data/
│   ├── raw/
│   │   └── steam-200k.csv
│   └── processed/
│       ├── user_features.csv
│       ├── clustered_users.csv
│       └── model_results.csv
├── notebooks/
│   ├── 01_data_loading_and_eda.ipynb
│   ├── 02_feature_engineering_and_clustering.ipynb
│   └── 03_modeling_and_evaluation.ipynb
├── outputs/
│   ├── figures/
│   ├── models/
│   └── reports/
├── src/
│   ├── __init__.py
│   ├── config.py
│   └── data_processing.py
├── app.py
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

The `outputs/` folder is kept for optional figures, reports, and model artifacts. The main dashboard-ready outputs are stored under `data/processed/`.

---

## Project Workflow

The project follows this workflow:

1. Load the raw Steam user-game interaction data.
2. Perform basic data checks and exploratory data analysis.
3. Clean and prepare the dataset.
4. Convert interaction-level data into user-level behavioral features.
5. Scale the behavioral features before clustering.
6. Use K-Means clustering to discover user segments.
7. Use elbow method and silhouette score to evaluate the cluster structure.
8. Use PCA to visualize the clusters in two dimensions.
9. Use supervised models to reproduce and explain the K-Means cluster labels.
10. Compare the models with a DummyClassifier baseline.
11. Use Decision Tree feature importance and confusion matrix for interpretability.
12. Present the results in an interactive Streamlit dashboard.
13. Make the project runnable with Docker and Docker Compose.

---

## Notebooks

### 01_data_loading_and_eda.ipynb

This notebook focuses on understanding the raw dataset. It includes data loading, basic data checks, missing value and duplicate checks, purchase/play action analysis, top games, user interaction patterns, and basic visualizations.

### 02_feature_engineering_and_clustering.ipynb

This notebook converts raw Steam interactions into user-level behavioral features. It then applies scaling, K-Means clustering, elbow method, silhouette score analysis, PCA visualization, cluster profile interpretation, and saves the clustered user data.

### 03_modeling_and_evaluation.ipynb

This notebook focuses on supervised model comparison and interpretability. The K-Means cluster labels are used as a target-like variable to check whether the discovered segments can be reproduced and explained using behavioral features.

Models used:

* DummyClassifier
* Logistic Regression
* KNN
* Decision Tree
* Random Forest
* Gradient Boosting

Evaluation includes:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion matrix
* Classification report
* Feature importance

---

## Feature Engineering

The following user-level features are created:

| Feature              | Description                                     |
| -------------------- | ----------------------------------------------- |
| `total_hours`        | Total play hours of the user                    |
| `avg_hours`          | Average play hours across play interactions     |
| `max_hours`          | Maximum playtime for a single game              |
| `unique_games`       | Number of unique games associated with the user |
| `purchase_count`     | Number of purchase interactions                 |
| `total_interactions` | Total number of user-game interactions          |
| `hours_per_game`     | Average playtime per unique game                |
| `purchase_ratio`     | Share of interactions that are purchases        |

These features represent three main behavioral dimensions:

* Engagement intensity
* Library diversity
* Purchasing behavior

This feature engineering step is important because the raw dataset does not directly describe users. It only records actions. The created features turn these actions into a more meaningful user profile.

---

## Clustering Approach

Since the dataset does not include predefined user type labels, I first used K-Means clustering to discover behavioral user segments.

The cluster labels are numeric at first, such as Cluster 0, Cluster 1, Cluster 2, and Cluster 3. These labels are not meaningful by themselves. To interpret them, I looked at the average feature values of each cluster.

The final segment names are:

* Moderate / Regular Players
* Low Engagement / Mostly Purchasers
* Broad Library / Collectors
* Focused Heavy Players

These names were assigned based on the cluster profile statistics such as playtime, purchase ratio, number of games, and hours per game.

---

## Modeling Approach

The supervised learning part uses the K-Means cluster labels as a target-like variable. This part should be interpreted carefully.

The model is not predicting an external ground-truth user type. Instead, it measures how well the discovered K-Means segments can be reproduced and explained using the behavioral features.

In other words:

**K-Means is used for discovery. Decision Tree and other classifiers are used for explanation and consistency checking.**

This is why high model scores should not be interpreted as real-world predictive accuracy. They show that the clusters are clearly separated in the behavioral feature space.

---

## Model Evaluation

The models are evaluated with accuracy, precision, recall, and F1-score. Since the cluster sizes are not perfectly balanced, weighted precision, recall, and F1-score are used.

A DummyClassifier is included as a baseline. This shows what performance looks like when the model does not really learn behavioral patterns and mostly follows the most frequent class.

The Decision Tree is analyzed in more detail because it is easier to interpret than more complex models. It helps show which features are most important for separating the discovered user segments.

---

## Main Result

The main result of this project is that Steam users cannot be explained only by total playtime.

The analysis shows that purchasing behavior, game diversity, and playtime intensity all matter. One of the strongest findings is that `purchase_ratio` is the most important feature in the Decision Tree interpretation.

This means that the balance between purchasing games and actually playing them is a key factor in explaining different Steam user segments.

In short, the project turns raw Steam interaction data into explainable user segments and shows which behavioral features separate these user groups.

---

## Streamlit Dashboard

The project includes an interactive Streamlit dashboard in `app.py`.

The dashboard includes:

* Project overview
* Data summary
* User-level feature preview
* Feature distribution charts
* Cluster distribution
* Cluster profile table
* Model comparison results
* Decision Tree feature importance
* Decision Tree confusion matrix

The dashboard reads the processed CSV files from `data/processed/`, so it opens quickly and does not retrain the models every time.

---

## Running Locally

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the Streamlit dashboard:

```bash
streamlit run app.py --server.port=8502
```

Then open:

```text
http://localhost:8502
```

---

## Running with Docker

Build the Docker image:

```bash
docker build -t steam-user-segmentation-dashboard .
```

Run the container:

```bash
docker run -p 8502:8502 steam-user-segmentation-dashboard
```

Then open:

```text
http://localhost:8502
```

---

## Running with Docker Compose

You can also run the project with Docker Compose:

```bash
docker compose up --build
```

Then open:

```text
http://localhost:8502
```

---

## Requirements

The main Python packages used in this project are:

* numpy
* pandas
* matplotlib
* plotly
* streamlit
* scikit-learn
* scipy

The dependencies are listed in `requirements.txt`.

---

## Limitations

There are a few limitations to keep in mind.

First, the cluster labels are created by K-Means, not by external user labels. Therefore, the supervised model results should be interpreted as internal consistency and explainability of the segmentation, not as external predictive generalization.

Second, different feature choices or a different number of clusters could produce different segment structures.

Third, the dashboard focuses on already processed outputs. This makes the app faster and easier to run in Docker, but the full analysis process is shown in the notebooks.

---

## Course Relevance

This project combines several topics from DS570 in one workflow:

* Data processing
* Exploratory data analysis
* Data visualization
* Feature engineering
* Clustering
* PCA
* Supervised machine learning
* Model evaluation
* Model interpretability
* Streamlit dashboard development
* Git/GitHub version control
* Docker containerization

The goal was not only to build a model, but to create an understandable end-to-end data science project that can be explored through a dashboard and reproduced with Docker.
