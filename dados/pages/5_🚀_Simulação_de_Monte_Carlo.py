import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import date
from util import DataDashboard

# Instanciar a classe do dashboard
data_dashboard = DataDashboard()

# Configurações da página do Streamlit
st.set_page_config(layout="wide",
                   page_title="Simulação de Monte Carlo",
                   page_icon="🚀")

# Carregar os dados históricos necessários
dados_1d = data_dashboard.bancoDeDados(symbol='BTCUSDT')

# Configuração de parâmetros da simulação
dias_posteriores = 100
simulacoes = 100

# Calcular o retorno acumulado e suas métricas
retorno_diario = dados_1d['retorno']
log_retorno_diario = (np.log(dados_1d["Close"]) - np.log(dados_1d["Close"]).shift(-1)).dropna()
log_media_retorno_diario = np.mean(log_retorno_diario)
log_desvio_retorno_diario = np.std(log_retorno_diario)

# Último preço disponível
ultimo_preco = dados_1d['Close'].tail(1).values[0]

# Realizar as simulações de Monte Carlo
results = np.empty((simulacoes, dias_posteriores))
for s in range(simulacoes):
    random_returns = 1 + np.random.normal(loc=log_media_retorno_diario, 
                                          scale=log_desvio_retorno_diario, 
                                          size=dias_posteriores)
    result = ultimo_preco * (random_returns.cumprod())
    results[s, :] = result

# Definir o índice da série simulada
index = pd.date_range(date.today().__str__(), periods=dias_posteriores, freq="D")
resultados = pd.DataFrame(results.T, index=index)
media_resultados = resultados.apply("mean", axis=1)

# Adicionar métricas
st.header("Métricas da Simulação de Monte Carlo")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Último Preço", value=f"${ultimo_preco:,.2f}")
with col2:
    st.metric(label="Retorno Médio Diário", value=f"{(np.mean(retorno_diario) * 100):.4f}%")
with col3:
    st.metric(label="Desvio Padrão do Retorno Diário", value=f"{(np.std(retorno_diario) * 100):.4f}%")
with col4:
    st.metric(label="Previsão Média em 100 dias", value=f"${media_resultados[-1]:,.2f}")

# Definir o último mês do histórico
historico_mensal = dados_1d["Close"].last("2M")

# Início da Previsão
previsao_inicio = resultados.index[0]

# Criar o gráfico
fig = go.Figure()

# Adicionar o histórico do último mês
fig.add_trace(go.Scatter(
    x=historico_mensal.index,
    y=historico_mensal,
    mode='lines',
    name='Preço Histórico Último Mês',
    line=dict(color='black', width=2)
))

# Adicionar as simulações de Monte Carlo
for s in range(simulacoes):
    fig.add_trace(go.Scatter(
        x=resultados.index,
        y=resultados.iloc[:, s],
        mode='lines',
        line=dict(width=0.5, color='blue'),
        opacity=0.3,
        showlegend=False
    ))

# Adicionar a linha do último preço
fig.add_trace(go.Scatter(
    x=[previsao_inicio, resultados.index[-1]],
    y=[ultimo_preco, ultimo_preco],
    mode='lines',
    line=dict(color='orange', dash='dash'),
    name='Último Preço'
))

# Resultado Médio e Desvios
fig.add_trace(go.Scatter(
    x=resultados.index,
    y=media_resultados,
    mode='lines',
    line=dict(width=2, color='red'),
    name='Previsão Média'
))

# 2x Desvio Padrão Superior
fig.add_trace(go.Scatter(
    x=resultados.index,
    y=media_resultados.apply(lambda x: x * (1 + 1.96 * log_desvio_retorno_diario)),
    mode='lines',
    line=dict(width=2, color='gray', dash='dot'),
    name='2x Desvio Padrão Superior'
))

# 2x Desvio Padrão Inferior
fig.add_trace(go.Scatter(
    x=resultados.index,
    y=media_resultados.apply(lambda x: x * (1 - 1.96 * log_desvio_retorno_diario)),
    mode='lines',
    line=dict(width=2, color='gray', dash='dot'),
    name='2x Desvio Padrão Inferior'
))

# Configuração dos títulos e layout
fig.update_layout(
    title=f"Simulação Monte Carlo - {simulacoes} Cenários",
    xaxis_title="Data",
    yaxis_title="Preço",
    showlegend=True,
    height=600,
    template="plotly_white"
)

# Adicionar o grid ao layout e melhorar a legibilidade
fig.update_xaxes(showgrid=True, gridcolor='LightGray', tickformat="%d-%b")
fig.update_yaxes(showgrid=True, gridcolor='LightGray')

# Mostrar o gráfico no Streamlit
st.plotly_chart(fig)
