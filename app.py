import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="DS570 Steam User Analysis",
    layout="wide"
)

st.title("DS570 Final Project")
st.subheader("Explainable Steam User Segmentation and Game Recommendation Dashboard")

st.write(
    "This project analyzes Steam users' gameplay and purchasing behavior "
    "to identify user segments, explain behavioral patterns, and explore "
    "game-to-game associations."
)

st.info("Project structure has been initialized. Analysis modules and dashboard sections will be added step by step.")

st.header("Project Modules")

modules = pd.DataFrame({
    "Module": [
        "Data Processing",
        "Exploratory Data Analysis",
        "User Segmentation",
        "Predictive Modeling",
        "Association Rules",
        "Dashboard",
        "Docker"
    ],
    "Status": [
        "Planned",
        "Planned",
        "Planned",
        "Planned",
        "Planned",
        "Initialized",
        "Initialized"
    ]
})

st.dataframe(modules, use_container_width=True)
