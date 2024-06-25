import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from util import DataDashboard

st.set_page_config(layout="wide", page_title="FinanceIN")
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

with st.sidebar:
    st.image("./Page/assets/logo.png")

st.sidebar.divider()
if st.sidebar.button("Home"):
    col_l, col_c, col_r = st.columns(3)
    
    with col_c:
        st.image("./Page/assets/logo.png", width=300, use_column_width=True)
        st.markdown("<h1 style='text-align: center;'>Dashboard Criptomoedas</h1>", unsafe_allow_html=True)

st.sidebar.divider()
if st.sidebar.button("Analise de Retornos"):
    st.title("Dashboard Cripto")

    ativos = ['BTC', 'ETH', 'MATIC', 'NEAR', 'MANA', 'RNDR', 'ADA', 'LINK',
            'FET', 'GALA', 'VET', 'MKR', 'FIL', 'SOL', 'DOT', 'AGIX', 'AVAX',
            'PENDLE', 'THETA', 'SHIB', 'TON', 'OP', 'BNB', 'ICP']

    option = st.selectbox('Escolha uma Criptomoeda: ', ativos)

    data_dashboard = DataDashboard()
    dados_cripto = data_dashboard.bancoDeDados(symbol=f'{option}USDT')

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Dados de {option}")
        st.dataframe(dados_cripto, use_container_width=True)

    with col2:
        st.subheader(f"Retorno e Retorno Acumulado de {option}")
        st.line_chart(dados_cripto, y=['retorno', 'retorno_diario_acumulado'])

    st.header("Análises Agregadas")

    col3, col4, col5 = st.columns(3)

    with col3:
        gmes = dados_cripto.groupby('mes').agg({'retorno': 'sum'})
        st.subheader("Rentabilidade por Mês")
        st.bar_chart(gmes)

    with col4:
        gdia = dados_cripto.groupby('dia').agg({'retorno': 'sum'})
        st.subheader("Rentabilidade por Dia")
        st.bar_chart(gdia)

    with col5:
        gweek = dados_cripto.groupby('weekday').agg({'retorno': 'sum'})
        st.subheader("Rentabilidade por Dia da Semana")
        st.bar_chart(gweek)

    st.header("Análises de Risco e Retorno")

    col6, col7 = st.columns(2)

    with col6:
        gvar_week = dados_cripto.groupby('weekday').agg({'retorno': 'var'})
        st.subheader("Volatilidade por Dia da Semana")
        st.bar_chart(gvar_week)

    with col7:
        st.subheader("Histograma de Retornos")
        fig = px.histogram(dados_cripto, x='retorno', nbins=75)
        st.plotly_chart(fig, use_container_width=True)

    st.header("Comparação com Índices de Mercado")

    sp500 = data_dashboard.get_close_data('^GSPC')
    ibove = data_dashboard.get_close_data('^BVSP')

    # Aqui você pode adicionar gráficos comparativos com SP500 e IBOVESPA

    st.header("Métricas de Risco e Retorno")

    retorno_medio = dados_cripto['retorno'].mean()
    risco = dados_cripto['retorno'].std()
    retorno_acumulado = dados_cripto['retorno_diario_acumulado'].iloc[-1]

    col8, col9, col10 = st.columns(3)

    col8.metric("Retorno Médio", f"{retorno_medio:.2%}")
    col9.metric("Risco (Desvio Padrão)", f"{risco:.2%}")
    col10.metric("Retorno Acumulado", f"{retorno_acumulado:.2%}")

    # Adicione aqui o gráfico de bolha para Risco x Retorno x Valorização

    # st.header("Preço de Aquisição vs P/L")
    # Adicione aqui o gráfico de barras empilhadas para Preço de aquisição vs P/L

st.sidebar.divider()
if st.sidebar.button("Teste"):
    pass
st.sidebar.divider()
