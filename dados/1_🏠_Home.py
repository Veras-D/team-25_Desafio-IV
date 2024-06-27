import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
from util import DataDashboard


st.set_page_config(layout="wide", 
                   page_title="Home",
                   page_icon="🏠")

st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)

col_l, col_c, col_r = st.columns(3)

with col_c:
    st.image("./Page/assets/logo.png", width=300, use_column_width=True)
    st.markdown("<h1 style='text-align: center;'>Dashboard Criptomoedas</h1>", unsafe_allow_html=True)
