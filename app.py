from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).parent
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


CLUSTER_NAMES = {
    0: "Moderate / Regular Players",
    1: "Low Engagement / Mostly Purchasers",
    2: "Broad Library / Collectors",
    3: "Focused Heavy Players"
}


@st.cache_data
def load_data():
    user_features_path = PROCESSED_DATA_DIR / "user_features.csv"
    clustered_users_path = PROCESSED_DATA_DIR / "clustered_users.csv"
    model_results_path = PROCESSED_DATA_DIR / "model_results.csv"

    user_features = pd.read_csv(user_features_path)
    clustered_users = pd.read_csv(clustered_users_path)
    model_results = pd.read_csv(model_results_path)

    model_name_map = {
        "dummy Classifier": "Dummy Classifier",
        "Dummy Classifier": "Dummy Classifier",
        "logistic Regression": "Logistic Regression",
        "Logistic Regression": "Logistic Regression",
        "KNN": "KNN",
        "decision Tree": "Decision Tree",
        "Decision Tree": "Decision Tree",
        "random Forest": "Random Forest",
        "Random Forest": "Random Forest",
        "gradient Boosting": "Gradient Boosting",
        "Gradient Boosting": "Gradient Boosting"
    }

    model_results["Model"] = model_results["Model"].replace(model_name_map)

    clustered_users["cluster_name"] = clustered_users["cluster"].map(CLUSTER_NAMES)

    return user_features, clustered_users, model_results


st.set_page_config(
    page_title="DS570 Steam User Segmentation",
    layout="wide"
)

st.title("DS570 Final Project")
st.subheader("Explainable Steam User Segmentation Dashboard")

st.write(
    "This project analyzes Steam users' purchasing and gameplay behavior. "
    "The main goal is to transform raw user-game interactions into user-level behavioral features, "
    "discover user segments with K-Means, and explain these segments with supervised models and "
    "Decision Tree interpretability."
)

try:
    user_features, clustered_users, model_results = load_data()
except FileNotFoundError as error:
    st.error("A required processed data file is missing.")
    st.write(error)
    st.stop()


tab_overview, tab_data, tab_clusters, tab_models, tab_insights = st.tabs([
    "Project Overview",
    "Data Summary",
    "User Segments",
    "Model Evaluation",
    "Decision Tree Insights"
])


with tab_overview:
    st.header("Project Overview")

    st.markdown(
        """
        The project follows an end-to-end data science workflow:

        1. Load and clean the Steam user-game interaction dataset.
        2. Convert raw interactions into user-level behavioral features.
        3. Use K-Means clustering to discover user segments without predefined labels.
        4. Interpret the clusters using summary statistics and PCA visualization.
        5. Use supervised models to reproduce and explain the discovered K-Means segments.
        6. Use Decision Tree analysis to make the segmentation logic more interpretable.
        """
    )

    st.info(
        "The supervised models do not predict external ground-truth user types. "
        "They reproduce K-Means cluster labels to check whether the discovered segments "
        "are consistent and explainable from the selected behavioral features."
    )

    modules = pd.DataFrame({
        "Module": [
            "Data Processing",
            "Exploratory Data Analysis",
            "User-Level Feature Engineering",
            "K-Means User Segmentation",
            "PCA Cluster Visualization",
            "Supervised Model Comparison",
            "Decision Tree Explainability",
            "Streamlit Dashboard",
            "Docker"
        ],
        "Status": [
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed"
        ]
    })

    st.dataframe(modules, use_container_width=True)


with tab_data:
    st.header("Data Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Users", f"{user_features['user_id'].nunique():,}")
    col2.metric("User Feature Rows", f"{len(user_features):,}")
    col3.metric("Behavioral Features", "8")
    col4.metric("Clusters", clustered_users["cluster"].nunique())

    st.subheader("User-Level Feature Table")
    st.dataframe(user_features.head(20), use_container_width=True)

    st.subheader("Feature Summary Statistics")
    feature_columns = [
        "total_hours",
        "avg_hours",
        "max_hours",
        "unique_games",
        "purchase_count",
        "total_interactions",
        "hours_per_game",
        "purchase_ratio"
    ]

    st.dataframe(
        user_features[feature_columns].describe().T,
        use_container_width=True
    )

    st.subheader("Feature Distribution")

    selected_feature = st.selectbox(
        "Select a feature to visualize",
        feature_columns,
        index=0
    )

    fig = px.histogram(
        user_features,
        x=selected_feature,
        nbins=50,
        title=f"Distribution of {selected_feature}"
    )

    st.plotly_chart(fig, use_container_width=True)


with tab_clusters:
    st.header("User Segments")

    st.write(
        "The clusters were created with K-Means using the selected user-level behavioral features. "
        "The numeric cluster labels were interpreted by looking at the average behavior profile of each cluster."
    )

    cluster_counts = (
        clustered_users
        .groupby(["cluster", "cluster_name"])
        .size()
        .reset_index(name="user_count")
        .sort_values("cluster")
    )

    st.subheader("Cluster Distribution")
    st.dataframe(cluster_counts, use_container_width=True)

    fig = px.bar(
        cluster_counts,
        x="cluster_name",
        y="user_count",
        title="Number of Users by Cluster",
        labels={
            "cluster_name": "Cluster",
            "user_count": "Number of Users"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Cluster Profiles")

    cluster_profile = (
        clustered_users
        .groupby(["cluster", "cluster_name"])[feature_columns]
        .mean()
        .reset_index()
    )

    st.dataframe(
        cluster_profile.round(2),
        use_container_width=True
    )

    st.markdown(
        """
        **Cluster interpretation:**

        - **Moderate / Regular Players:** Users with moderate playtime and regular interaction patterns.
        - **Low Engagement / Mostly Purchasers:** Users with high purchase ratio but lower playtime engagement.
        - **Broad Library / Collectors:** Users with many unique games and high purchase counts.
        - **Focused Heavy Players:** Users with very high hours per game, usually focused on fewer games.
        """
    )

    st.subheader("Compare Cluster Feature Averages")

    selected_cluster_feature = st.selectbox(
        "Select a feature for cluster comparison",
        feature_columns,
        index=7
    )

    fig = px.bar(
        cluster_profile,
        x="cluster_name",
        y=selected_cluster_feature,
        title=f"Average {selected_cluster_feature} by Cluster",
        labels={
            "cluster_name": "Cluster",
            selected_cluster_feature: f"Average {selected_cluster_feature}"
        }
    )

    st.plotly_chart(fig, use_container_width=True)


with tab_models:
    st.header("Model Evaluation")

    st.write(
        "The supervised models use the K-Means cluster labels as a target-like variable. "
        "The purpose is to check whether the discovered segments can be reproduced from the behavioral features."
    )

    st.subheader("Model Results")
    st.dataframe(
        model_results.sort_values("F1 Score", ascending=False),
        use_container_width=True
    )

    fig = px.bar(
        model_results,
        x="Model",
        y=["Accuracy", "F1 Score"],
        barmode="group",
        title="Model Comparison on Test Set",
        labels={
            "value": "Score",
            "variable": "Metric"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        The Dummy Classifier is used as a baseline. It predicts the most frequent cluster
        and does not learn behavioral patterns. The supervised models perform much better
        than this baseline, which shows that the selected behavioral features can reproduce
        the K-Means segments.

        These scores should be interpreted carefully because the target is not an external
        ground-truth label. It is the K-Means cluster label created from the same behavioral
        feature set.
        """
    )


with tab_insights:
    st.header("Decision Tree Insights")

    st.write(
        "Decision Tree is included mainly for interpretability. It helps explain which behavioral features "
        "are useful for reproducing the K-Means user segments."
    )

    st.subheader("Key Findings")

    st.markdown(
        """
        - The Decision Tree reproduced most K-Means cluster labels very well.
        - Cluster 3 was relatively harder to separate than the other clusters.
        - Feature importance showed that **purchase_ratio** was the most important variable.
        - This means the balance between purchasing and playing behavior is a key factor in explaining the user segments.
        """
    )

    feature_importance = pd.DataFrame({
        "Feature": [
            "purchase_ratio",
            "total_interactions",
            "avg_hours",
            "max_hours",
            "hours_per_game",
            "total_hours",
            "purchase_count",
            "unique_games"
        ],
        "Importance": [
            0.762628,
            0.090501,
            0.081997,
            0.046394,
            0.009282,
            0.007520,
            0.001513,
            0.000165
        ]
    })

    st.subheader("Decision Tree Feature Importance")
    st.dataframe(feature_importance, use_container_width=True)

    fig = px.bar(
        feature_importance.sort_values("Importance"),
        x="Importance",
        y="Feature",
        orientation="h",
        title="Decision Tree Feature Importance"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        The most important insight is that the clusters are not only separated by total playtime.
        The **purchase_ratio** feature strongly separates users by showing whether their behavior
        is more purchase-heavy or play-heavy.

        This supports the main project idea: Steam user behavior should be analyzed through
        multiple behavioral dimensions, not only total hours played.
        """
    )

    st.subheader("Decision Tree Confusion Matrix")

    confusion_matrix_df = pd.DataFrame(
        [
            [1868, 0, 1, 2],
            [5, 481, 0, 0],
            [2, 0, 47, 0],
            [12, 1, 0, 60]
        ],
        index=[
            "Actual Cluster 0",
            "Actual Cluster 1",
            "Actual Cluster 2",
            "Actual Cluster 3"
        ],
        columns=[
            "Predicted Cluster 0",
            "Predicted Cluster 1",
            "Predicted Cluster 2",
            "Predicted Cluster 3"
        ]
    )

    st.dataframe(confusion_matrix_df, use_container_width=True)

    fig = px.imshow(
        confusion_matrix_df,
        text_auto=True,
        title="Decision Tree Confusion Matrix",
        labels=dict(x="Predicted Cluster", y="Actual Cluster", color="Count")
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        The confusion matrix shows that the Decision Tree reproduces the K-Means clusters very well.
        Most predictions are on the diagonal, meaning that the predicted cluster matches the actual
        K-Means cluster label.

        Cluster 0, Cluster 1, and Cluster 2 are predicted with very few errors. Cluster 3 is the
        relatively hardest segment to separate: some actual Cluster 3 users are predicted as Cluster 0.
        This suggests that a small group of **Focused Heavy Players** have behavioral values close to
        **Moderate / Regular Players**.
        """
    )
