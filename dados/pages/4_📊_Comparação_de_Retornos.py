import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from util import DataDashboard

data_dashboard = DataDashboard()

st.set_page_config(layout="wide",
                   page_title="Comparação de Retornos",
                   page_icon="📊")

ativos = ['ETH', 'MATIC', 'NEAR', 'MANA', 'RNDR', 'ADA', 'LINK',
        'FET', 'GALA', 'VET', 'MKR', 'FIL', 'SOL', 'DOT', 'AGIX', 'AVAX',
        'PENDLE', 'THETA', 'SHIB', 'TON', 'OP', 'BNB', 'ICP']

# Inicializar o estado da seleção se ainda não existir
if 'selected_crypto_comparison' not in st.session_state:
    st.session_state.selected_crypto_comparison = 'ETH'  # Valor padrão

def update_selection_comparison():
    st.session_state.selected_crypto_comparison = st.session_state.crypto_selectbox_comparison

option = st.selectbox('Escolha uma Criptomoeda: ', ativos, 
                        key='crypto_selectbox_comparison',
                        index=ativos.index(st.session_state.selected_crypto_comparison),
                        on_change=update_selection_comparison)

dados_cripto = data_dashboard.bancoDeDados(symbol=f'{st.session_state.selected_crypto_comparison}USDT').tail(713)

btc = data_dashboard.bancoDeDados().tail(713)
sp500 = data_dashboard.get_close_data('^GSPC')
ibove = data_dashboard.get_close_data('^BVSP')

dados_cripto['Rentabilidade'] = dados_cripto['Close'] / dados_cripto['Close'].iloc[0]
btc['Rentabilidade'] = btc['Close'] / btc['Close'].iloc[0]
sp500['Rentabilidade'] = sp500['Close'] / sp500['Close'].iloc[0]
ibove['Rentabilidade'] = ibove['Close'] / ibove['Close'].iloc[0]

fig = go.Figure()

fig.add_trace(go.Scatter(x=dados_cripto.index, y=dados_cripto['Rentabilidade'], mode='lines', name=f'{st.session_state.selected_crypto_comparison}'))
fig.add_trace(go.Scatter(x=btc.index, y=btc['Rentabilidade'], mode='lines', name='BTC'))
fig.add_trace(go.Scatter(x=sp500.index, y=sp500['Rentabilidade'], mode='lines', name='S&P 500'))
fig.add_trace(go.Scatter(x=ibove.index, y=ibove['Rentabilidade'], mode='lines', name='IBOVESPA'))

fig.update_layout(
    title='Comparação de Rentabilidade',
    xaxis_title='Data',
    yaxis_title='Rentabilidade',
    legend_title='Ativo',
    template='plotly_dark'
)

st.plotly_chart(fig)
