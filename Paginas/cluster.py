import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path, low_memory=False)
    return df


def pagina_cluster():
    st.title("Pagina cluster")
    st.write("Pagina de cluster")