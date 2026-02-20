import json
import pandas as pd

# ========== CARREGAR DADOS ============
perfil = json.load(open('./data/diretrizes_economicas.json'))
transacoes = pd.read_csv('./data/execucao_orcamentaria.csv')
historico = pd.read_csv('./data/historico_intervencoes.csv')
produtos = json.load(open('./data/instrumentos_macro.json'))