import streamlit as st
import plotly.express as px
from util import DataDashboard

data_dashboard = DataDashboard()

st.set_page_config(layout="wide",
                   page_title="Analise de Retornos",
                   page_icon="🔍")

st.title("Dashboard Cripto")

ativos = ['BTC', 'ETH', 'MATIC', 'NEAR', 'MANA', 'RNDR', 'ADA', 'LINK',
        'FET', 'GALA', 'VET', 'MKR', 'FIL', 'SOL', 'DOT', 'AGIX', 'AVAX',
        'PENDLE', 'THETA', 'SHIB', 'TON', 'OP', 'BNB', 'ICP']

# Inicializar o estado da seleção se ainda não existir
if 'selected_crypto' not in st.session_state:
    st.session_state.selected_crypto = 'BTC'  # Valor padrão

def update_selection():
    st.session_state.selected_crypto = st.session_state.crypto_selectbox

option = st.selectbox('Escolha uma Criptomoeda: ', ativos, 
                        key='crypto_selectbox',
                        index=ativos.index(st.session_state.selected_crypto),
                        on_change=update_selection)

dados_cripto = data_dashboard.bancoDeDados(symbol=f'{st.session_state.selected_crypto}USDT')

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Dados de {st.session_state.selected_crypto}")
    st.dataframe(dados_cripto, use_container_width=True)

with col2:
    st.subheader(f"Retorno e Retorno Acumulado de {st.session_state.selected_crypto}")
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


# Adicione aqui o gráfico de bolha para Risco x Retorno x Valorização

# st.header("Preço de Aquisição vs P/L")
# Adicione aqui o gráfico de barras empilhadas para Preço de aquisição vs P/L