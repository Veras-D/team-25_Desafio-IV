import streamlit as st
import plotly.express as px
from util import DataDashboard

data_dashboard = DataDashboard()

st.set_page_config(layout="wide",
                   page_title="Simulação de Monte Carlo",
                   page_icon="🚀")
