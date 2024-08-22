import streamlit as st
import plotly.express as px
from util import DataDashboard

# Instanciar a classe do dashboard
data_dashboard = DataDashboard()

# Configurar a página do Streamlit
st.set_page_config(layout="wide",
                   page_title="Macro Economia",
                   page_icon="🏛️")

# Carregar dados macroeconômicos
lista = data_dashboard.get_dado_historica_USA()
dominance = round(data_dashboard.get_BTC_dominance() * 100, 2)
fear_and_greed_index, status = data_dashboard.get_fear_and_greed_index()

# Cabeçalho da página
st.header("Dados Macro Econômicos")

# Colunas para métricas principais
col1, col2 = st.columns(2)
with col1:
    st.metric('Dominância do BTC (%)', dominance)
with col2:
    st.metric(f'Índice de Medo e Ganância: {status.upper()}', fear_and_greed_index)

# Garantir que a criptomoeda selecionada esteja no estado da sessão
if 'selected_crypto' not in st.session_state:
    st.session_state.selected_crypto = 'BTC'  # Valor padrão, se necessário

# Carregar dados de criptomoeda com base na seleção
dados_cripto = data_dashboard.bancoDeDados(symbol=f'{st.session_state.selected_crypto}USDT')
retorno_medio = dados_cripto['retorno'].mean()
risco = dados_cripto['retorno'].std()
retorno_acumulado = dados_cripto['retorno_diario_acumulado'].iloc[-1]

# Exibir métricas de risco e retorno
st.header("Métricas de Risco e Retorno BTC")
col8, col9, col10 = st.columns(3)
with col8:
    st.metric("Retorno Médio", f"{retorno_medio:.2%}")
with col9:
    st.metric("Risco (Desvio Padrão)", f"{risco:.2%}")
with col10:
    st.metric("Retorno Acumulado", f"{retorno_acumulado:.2%}")

# Gráficos para dados macroeconômicos
col3, col4, col5 = st.columns(3)
with col3:
    st.header("Taxa de Juros dos EUA")
    st.plotly_chart(px.line(lista[0], title="Taxa de Juros dos EUA"))
with col4:
    st.header("Taxa de Desemprego EUA")
    st.plotly_chart(px.line(lista[3], title="Taxa de Desemprego EUA"))
with col5:
    st.header("Índice de Confiança do Consumidor EUA")
    st.plotly_chart(px.line(lista[-1], title="Índice de Confiança do Consumidor EUA"))
