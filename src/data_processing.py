import pandas as pd


def load_steam_data(path):
    """
    Load the raw Steam user-game interaction dataset.

    The raw file has no header. Each row represents one user-game interaction.
    Expected columns:
    user_id, game, action, hours, unused
    """
    df = pd.read_csv(
        path,
        header=None,
        names=["user_id", "game", "action", "hours", "unused"]
    )

    return df


def clean_steam_data(df):
    """
    Apply basic cleaning steps to the raw Steam dataset.
    """
    df = df.copy()

    if "unused" in df.columns:
        df = df.drop("unused", axis=1)

    df["user_id"] = df["user_id"].astype(int)
    df["game"] = df["game"].astype(str)
    df["action"] = df["action"].astype(str)
    df["hours"] = pd.to_numeric(df["hours"], errors="coerce")

    df = df.dropna()
    df = df.drop_duplicates()

    return df


def create_user_features(df):
    """
    Aggregate raw user-game interactions into user-level behavioral features.
    """
    df = df.copy()

    df["play_hours"] = df["hours"].where(df["action"] == "play", 0)
    df["purchase_flag"] = (df["action"] == "purchase").astype(int)

    user_features = df.groupby("user_id").agg(
        total_hours=("play_hours", "sum"),
        avg_hours=("play_hours", "mean"),
        max_hours=("play_hours", "max"),
        unique_games=("game", "nunique"),
        purchase_count=("purchase_flag", "sum"),
        total_interactions=("action", "count")
    ).reset_index()

    user_features["hours_per_game"] = (
        user_features["total_hours"] / user_features["unique_games"]
    )

    user_features["purchase_ratio"] = (
        user_features["purchase_count"] / user_features["total_interactions"]
    )

    return user_features


def save_processed_data(df, path):
    """
    Save a processed dataframe as a CSV file.
    """
    df.to_csv(path, index=False)
