import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
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
data_dashboard = DataDashboard()

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
if st.sidebar.button("Dados Macro Econômicos"):
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

st.sidebar.divider()

if st.sidebar.button("Comparação de Retornos"):

    ativos = ['ETH', 'MATIC', 'NEAR', 'MANA', 'RNDR', 'ADA', 'LINK',
            'FET', 'GALA', 'VET', 'MKR', 'FIL', 'SOL', 'DOT', 'AGIX', 'AVAX',
            'PENDLE', 'THETA', 'SHIB', 'TON', 'OP', 'BNB', 'ICP']

    option = st.selectbox('Escolha uma Criptomoeda: ', ativos)

    dados_cripto = data_dashboard.bancoDeDados(symbol=f'{option}USDT')

    btc = data_dashboard.bancoDeDados()
    sp500 = data_dashboard.get_close_data('^GSPC')
    ibove = data_dashboard.get_close_data('^BVSP')
    
    dados_cripto['Rentabilidade'] = dados_cripto['Close'] / dados_cripto['Close'].iloc[0]
    btc['Rentabilidade'] = btc['Close'] / btc['Close'].iloc[0]
    sp500['Rentabilidade'] = sp500['Close'] / sp500['Close'].iloc[0]
    ibove['Rentabilidade'] = ibove['Close'] / ibove['Close'].iloc[0]
    # Criando o gráfico com Plotly
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dados_cripto.index, y=dados_cripto['Rentabilidade'], mode='lines', name=f'{option}'))
    fig.add_trace(go.Scatter(x=btc.index, y=btc['Rentabilidade'], mode='lines', name='BTC'))
    fig.add_trace(go.Scatter(x=sp500.index, y=sp500['Rentabilidade'], mode='lines', name='S&P 500'))
    fig.add_trace(go.Scatter(x=ibove.index, y=ibove['Rentabilidade'], mode='lines', name='IBOVESPA'))

    # Ajustando o layout do gráfico
    fig.update_layout(
        title='Comparação de Rentabilidade',
        xaxis_title='Data',
        yaxis_title='Rentabilidade',
        legend_title='Ativo',
        template='plotly_dark'
    )

    st.plotly_chart(fig)
st.sidebar.divider()
