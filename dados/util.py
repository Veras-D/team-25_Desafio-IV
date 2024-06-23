import pandas as pd
import numpy as np
import scipy
import requests
import json
import pandas_datareader.data as web
from datetime import datetime
import matplotlib.pyplot as plt
import yfinance as yf


class DataDashboard:
    def __init__(self, symbol: str = 'BTCUSDT', time_rec: str = '1d', window: int = 14):
        self.symbol = symbol
        self.time_rec = time_rec
        self.window = window


    def calculate_rsi(self, data):
        # Calcular as variações de preço
        deltas = data['Close'].diff()

        # Separar as variações de preço em positivas e negativas
        gain = deltas.where(deltas > 0, 0)
        loss = -deltas.where(deltas < 0, 0)

        # Calcular as médias móveis
        average_gain = gain.rolling(window=self.window, min_periods=1).mean()
        average_loss = loss.rolling(window=self.window, min_periods=1).mean()

        # Calcular o RSI
        rs = average_gain / average_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi


    # Verificar se a requisição foi bem-sucedida
    def bancoDeDados(self, time_rec: str = '1d', symbol: str = 'BTCUSDT'):
        requisicao = requests.get(f"https://api.binance.us/api/v3/klines?symbol={symbol}&interval={time_rec}&limit=1000")
        if requisicao.status_code == 200:
            dados_historicos = requisicao.json()

            # Converter dados em DataFrame
            colunas = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVolume', 'NumberOfTrades', 'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume', 'Ignore']  
            dados = pd.DataFrame(dados_historicos, columns=colunas).astype(float)
            dados.loc[dados['High'] == 138070.000000] = pd.NA
            dados = dados.ffill()
            # Converter o timestamp para datetime
            dados['Timestamp'] = pd.to_datetime(dados['Timestamp'], unit='ms').astype(str)
            dados['Timestamp'] = pd.DatetimeIndex(dados['Timestamp'])
            dados['ano'] = dados['Timestamp'].dt.year
            dados['mes'] = dados['Timestamp'].dt.month
            dados['dia'] = dados['Timestamp'].dt.day
            dados['weekday'] = dados['Timestamp'].dt.day_name()
            dados = dados.rename(columns={'Timestamp': 'Data'})
            # Definir o timestamp como índice do DataFrame
            dados = dados.set_index('Data')
            dados['mm55d'] = dados['Close'].rolling(55).mean()
            dados['mm12d'] = dados['Close'].rolling(12).mean()
            dados['mm26d'] = dados['Close'].rolling(26).mean()
            dados['MACD_linha'] = dados['mm12d'] - dados['mm26d']
            dados['MACD_media'] = dados['MACD_linha'].rolling(9).mean()
            dados['MACD_hist'] = dados['MACD_linha'] - dados['MACD_media']
            dados['retorno'] = dados['Close'] / dados['Close'].shift() - 1
            dados['retorno_diario_acumulado'] = (1 + dados['retorno']).cumprod() - 1
            # Aplicar a função calculate_rsi aos dados
            dados['RSI'] = self.calculate_rsi(dados)
            dados = dados.drop(columns=['Ignore', 'QuoteAssetVolume', 'CloseTime', 'TakerBuyBaseAssetVolume', 'NumberOfTrades', 'TakerBuyQuoteAssetVolume'])
            dados = dados[~dados['weekday'].isin(['Saturday', 'Sunday'])]
            
            return dados
    
        else:
            print(f"Erro ao fazer a requisição: {requisicao.status_code}")
            return None
    
    
    def get_fear_and_greed_index(self):
        response = requests.get('https://api.alternative.me/fng/')
        try:
            data = response.json()
            fear_and_greed_index = data['data'][0]['value']
            status = data['data'][0]['value_classification']
            return fear_and_greed_index, status
        except json.JSONDecodeError:
            print("Erro ao decodificar JSON. Verifique a resposta da API.")
            return None, None

    def get_BTC_dominance(self):
        response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false')
        response = response.json()

        #initialises variables
        BTCCap = 0
        altCap = 0
        current_time = datetime.now().strftime("%d-%m-%Y")
        #current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


        #iterates through response
        for x in response:
            #print(x['id'])
            if x['id'] == "bitcoin": #adds bitcoin market cap to BTCCap and altCap
                BTCCap = x['market_cap']
                altCap = altCap + x['market_cap']
            else: #adds any altcoin market cap to altCap
                altCap = altCap + x['market_cap']
                
        btc_dominance = BTCCap/altCap
        return btc_dominance
    
    
    def get_dado_historica_USA(self):
        # Definir o período para os dados que você deseja obter
        start = datetime(2000, 1, 1)
        end = datetime.now()

        # Obter os dados da taxa de juros do Fed (FEDFUNDS)
        fed = web.DataReader('FEDFUNDS', 'fred', start, end)
        
        # PIB dos EUA
        gdp = web.DataReader('GDP', 'fred', start, end)

        # Índice de Preços ao Consumidor
        cpi = web.DataReader('CPIAUCSL', 'fred', start, end)
        
        # Taxa de Desemprego
        unemployment_rate = web.DataReader('UNRATE', 'fred', start, end)

        # Índice de Produção Industrial
        industrial_production = web.DataReader('INDPRO', 'fred', start, end)

        # Taxa de Inflação
        inflation_rate = web.DataReader('T10YIE', 'fred', start, end)

        # Taxa de Câmbio do Dólar
        exchange_rate = web.DataReader('DEXUSEU', 'fred', start, end)

        # Dívida dos Consumidores
        consumer_debt = web.DataReader('TOTALSL', 'fred', start, end)

        # Preço do Petróleo
        oil_price = web.DataReader('DCOILWTICO', 'fred', start, end)

        # Confiança do Consumidor
        consumer_confidence = web.DataReader('UMCSENT', 'fred', start, end)

        return [fed, gdp, cpi, unemployment_rate, industrial_production, inflation_rate, consumer_debt, oil_price, consumer_confidence]


    def get_close_data(self, papel: str):
        papel = yf.Ticker(papel)
        hist = papel.history(period="max", interval = "1d")
        return hist['Close'].tail(713)
