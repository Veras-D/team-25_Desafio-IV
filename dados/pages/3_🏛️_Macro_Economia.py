import streamlit as st
import plotly.express as px
from util import DataDashboard

data_dashboard = DataDashboard()

st.set_page_config(layout="wide",
                   page_title="Macro Economia",
                   page_icon="🏛️")

lista = data_dashboard.get_dado_historica_USA()
dominance = round(data_dashboard.get_BTC_dominance() * 100, 2)
fear_and_greed_index, status = data_dashboard.get_fear_and_greed_index()
st.header("Dados Macro Econômicos")
col1, col2 = st.columns(2)
with col1:
    st.metric('Dominância do BTC (%)', dominance)
with col2:
    st.metric(f'Índice de Medo e Ganância: {status.upper()}', fear_and_greed_index)

col3, col4, col5 = st.columns(3)
with col3:
    st.header("Taxa de juros dos USA")
    st.plotly_chart(px.line(lista[0]))
with col4:
    st.header("Taxa de Desemprego USA")
    st.plotly_chart(px.line(lista[3]))
with col5:
    st.header("Índice de Confiança do Consumidor USA")
    st.plotly_chart(px.line(lista[-1]))
