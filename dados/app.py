import streamlit as st
import plotly.express as px
import pandas as pd
import matplatlib.pyplot as plt
from util import DataDashboard


st.header("Dashboard Cripto")

ativos = ['BTC', 'ETH', 'MATIC', 'INJ', 'NEAR', 'MANA', 'RNDR', 'ADA', 'LINK',
          'FET', 'GALA', 'VET', 'MKR', 'FIL', 'SOL', 'DOT', 'AGIX', 'AVAX',
          'PENDLE', 'THETA', 'SHIB', 'TON', 'OP', 'BNB', 'ICP']

data_dashboard = DataDashboard()
dados_cripto = data_dashboard.bancoDeDados()

plt.hist(dados_cripto['retorno'], bins = 75)
plt.show()

dados_cripto.groupby('mes').agg({'retorno': 'sum'}).plot(kind='bar')  # Melhor mes para investir (menor valor)  # Testar outro alem do sum  # Rentabilidade por mes
dados_cripto.groupby('dia').agg({'retorno': 'sum'}).plot(kind='bar')  # Melhor dia para investir (menor valor)
dados_cripto.groupby('weekday').agg({'retorno': 'sum'}).plot(kind='bar')  # Melhor dia da semana para investir (menor valor)
dados_cripto.groupby('weekday').agg({'retorno': 'var'}).plot(kind='bar')  # Dia da semana mais volatil (menor valor)

# Risco X retorno X Valorização (retono acumulado) (Grafico de bolha?)
retorno_var = dados_cripto['retorno'].mean()
risco = dados_cripto['retorno'].std()

# Preço de aquisição (fechamento) X P/L (df['close'] / df['rentabilidade'].iloc[-1]) stacked bar char

sp500 = data_dashboard.get_close_data('^GSPC')
ibove = data_dashboard.get_close_data('^BVSP')

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)
