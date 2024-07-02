import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

# Define o nome do dono do repositório e o nome do repositório
owner = 'veras-d'
repo = 'team-25_Desafio-IV'

# Define a data inicial como string e converte para objeto datetime
start_date = datetime.strptime("2024-06-29", "%Y-%m-%d")

# Listas para armazenar datas e contagens de commits
commit_dates = []

# Itera pelos últimos 30 dias
for i in range(30):
    # Calcula a data do dia atual no loop
    current_date = start_date - timedelta(days=i)
    next_day = current_date + timedelta(days=1)
    
    # URL da API do GitHub para obter commits
    url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    params = {
        'since': current_date.isoformat(),
        'until': next_day.isoformat()
    }

    # Faz a requisição GET para obter os commits
    response = requests.get(url, params=params)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        commits = response.json()
        # Adiciona a data dos commits à lista
        commit_dates.extend([datetime.strptime(commit['commit']['committer']['date'], '%Y-%m-%dT%H:%M:%SZ').date() for commit in commits])
    else:
        print(f"Falha ao obter commits: {response.status_code}")

# Conta os commits por dia usando pandas
commit_counts = pd.Series(commit_dates).value_counts().sort_index()

# Cria o gráfico
plt.figure(figsize=(10, 5))
plt.plot(commit_counts.index, commit_counts.values, marker='o')
plt.title('Quantidade de Commits por Dia no Último Mês')
plt.xlabel('Data')
plt.ylabel('Quantidade de Commits')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

