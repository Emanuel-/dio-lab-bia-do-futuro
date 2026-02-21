import json
import pandas as pd
import requests
import streamlit as st  # Ajustado

# ========= CONFIGURAÇÕES ==========
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss:20b-cloud" 

# ========= CARREGAR DADOS ==========
try:
    diretrizes = json.load(open('./data/diretrizes_economicas.json', encoding='utf-8'))
    orcamento = pd.read_csv('./data/execucao_orcamentaria.csv')
    intervencoes = pd.read_csv('./data/historico_intervencoes.csv')
    instrumentos = json.load(open('./data/instrumentos_macro.json', encoding='utf-8'))
except FileNotFoundError as e:
    st.error(f"Erro: Certifique-se de que os arquivos de dados estão na pasta './data/'. {e}")
    st.stop()

# ========= MONTA CONTEXTO ==========
diretriz_ativa = diretrizes[0] 

contexto = f"""
AGENTE: MANO (Macro Agente Nacional Operante)
DIRETRIZ ATUAL: {diretriz_ativa['perfil']}
PRIORIDADE: {diretriz_ativa['prioridade']}
FOCO: {diretriz_ativa['foco']}

EXECUÇÃO ORÇAMENTÁRIA ATUAL:
{orcamento.to_string(index=False)}

HISTÓRICO DE INTERVENÇÕES E CRISES:
{intervencoes.to_string(index=False)}

INSTRUMENTOS DE POLÍTICA DISPONÍVEIS:
{json.dumps(instrumentos, indent=2, ensure_ascii=False)}
"""

SYSTEM_PROMPT = """
OBJETIVO:
Ensinar conceitos de macroeconomia e gestão pública de forma simples, transformando dados técnicos do orçamento federal em exemplos práticos e compreensíveis.

REGRAS:
1. Neutralidade Política: Explique as consequências técnicas baseando-se nas diretrizes.
2. Dados Reais: Use a execução orçamentária para ilustrar conceitos.
3. Educação sobre Instrumentos: Explique Selic, Swaps e Títulos sem recomendar investimentos.
4. Tom de Voz: Linguagem amigável e didática, sem "economês" puro.
5. Transparência: Se não souber, admita e explique o conceito teórico.
6. Engajamento: Sempre termine com uma pergunta de verificação.
"""

# ========= FUNÇÃO DE CHAMADA =========
def perguntar_ao_mano(pergunta_usuario):
    prompt = f""" 
    {SYSTEM_PROMPT}
    
    SITUAÇÃO ECONÔMICA ATUAL (DADOS OFICIAIS):
    {contexto}
    
    PERGUNTA DO CIDADÃO: 
    {pergunta_usuario}
    
    RESPOSTA DO MANO:"""
    
    payload = {
        "model": MODELO,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7}
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json()['response']
    except Exception as e:
        return f"Erro ao conectar com o MANO: {str(e)}"

# =========== INTERFACE STREAMLIT ===========
st.set_page_config(page_title="MANO - Macro Agente", page_icon="🏛️")
st.title("🏛️ MANO: Macro Agente Nacional Operante")
st.caption("Seu guia didático sobre a economia do país")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if pergunta := st.chat_input("Pergunte algo sobre o orçamento ou economia..."):
    st.session_state.messages.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Consultando dados oficiais..."):
            resposta = perguntar_ao_mano(pergunta) # Nome da função corrigido aqui
            st.markdown(resposta)
    
    st.session_state.messages.append({"role": "assistant", "content": resposta})