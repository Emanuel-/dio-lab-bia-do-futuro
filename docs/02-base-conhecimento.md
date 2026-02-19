# Base de Conhecimento

## Dados Utilizados


| Arquivo | Formato | Descrição |
|---------|---------|-----------|
| `execucao_orcamentaria.csv` | CSV | Orçamento Geral da União: Registra a arrecadação de impostos (entradas) e os gastos públicos como saúde, educação e previdência (saídas). |
| `historico_intervencoes.csv` | CSV | Livro de Intervenções: Registra crises econômicas (inflação alta, queda do PIB) e como os órgãos (BACEN, Tesouro) "atenderam" essa demanda. |
| `diretrizes_economicas.json` | JSON | Regime Econômico: Define se o governo atual é focado em Austeridade (Conservador), Desenvolvimento (Arrojado) ou Bem-Estar Social. |
| `instrumentos_macro.json` | JSON | Catálogo de Fomento: Lista os instrumentos que o Estado usa para se financiar ou intervir, como Títulos Públicos, Swaps Cambiais e Crédito Subsidiado. |


---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

As modificações/trocas foram devido ao modelo ter como finalidade agora, falar sobre macroeconomia. Devido a isso, as substituições foram feitas em cima de dados atuais da economia brasileira.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Existem duas possibilidades, injetar os dados diretamente no prompt(ctrl + c, ctrl + v) ou carregar via código, como no exemplo abaixo.

```python
import pandas as pd
import json

# 1. Carregar os arquivos CSV (Dados Tabulares)
# Carrega a Execução Orçamentária (antigo transacoes.csv)
df_orcamento = pd.read_csv('data/execucao_orcamentaria.csv')

# Carrega o Histórico de Intervenções (antigo historico_atendimento.csv)
df_intervencoes = pd.read_csv('data/historico_intervencoes.csv')

# 2. Carregar os arquivos JSON (Dicionários/Listas)
# Carrega as Diretrizes Econômicas (antigo perfil_investidor.json)
with open('data/diretrizes_economicas.json', 'r', encoding='utf-8') as f:
    diretrizes = json.load(f)

# Carrega os Instrumentos Macro (antigo produtos_financeiros.json)
with open('data/instrumentos_macro.json', 'r', encoding='utf-8') as f:
    instrumentos = json.load(f)
```

[ex: Os JSON/CSV são carregados no início da sessão e incluídos no contexto do prompt]

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

**1. Cabeçalho de Status (Cards de Resumo)**
    No topo, o usuário vê os indicadores em tempo real processados a partir da execucao_orcamentaria.csv:

- Resultado Primário: [R$ +XX Bi] (Verde se Superávit, Vermelho se Déficit).

- Diretriz Ativa: [Austeridade] (Lido do diretrizes_economicas.json).

- Risco País: [Baixo] (Baseado nos ativos do instrumentos_macro.json).

**2. Painel Central (Gráfico e Chat)**
- Lado Esquerdo: Um gráfico de pizza ou barras mostrando a composição dos gastos (Saúde vs. Educação vs. Defesa).

- Lado Direito: Uma janela de chat onde o usuário pergunta: "Como a diretriz de austeridade afetou os investimentos em infraestrutura este mês?".

**3. Linha do Tempo (Feed de Eventos)**
    Na base, um feed extraído do historico_intervencoes.csv mostrando as últimas ações do Estado:

- [12/10] Intervenção: COPOM elevou Selic para conter inflação.

- [05/10] Alerta: Déficit de arrecadação detectado na Receita Federal.


---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.


```text
_________________________________________________________________________
| [ BRASIL: PAINEL MACRO ]          Perfil Atual: AUSTERIDADE (Fiscal)  |
|_______________________________________________________________________|
|                                                                       |
|  SALDO FISCAL (ACUMULADO)       GASTOS POR CATEGORIA (TOP 3)          |
|  [ #######----------- ]         1. Previdência [35%]                  |
|     R$ -15.4 Billhões           2. Pessoal     [25%]                  |
|                                 3. Juros Dívida[20%]                  |
|_______________________________________________________________________|
|                                                                       |
|  HISTÓRICO DE INTERVENÇÕES (Últimos Eventos)                          |
|  - [OK] Swap Cambial (Bacen) para conter alta do dólar                |
|  - [!]  Ajuste de meta fiscal em análise pelo Congresso               |
|_______________________________________________________________________|
|                                                                       |
|  IA ECONOMISTA: "Com base na diretriz de Austeridade, recomendo       |
|  contingenciamento na pasta de infraestrutura para fechar o mês."     |
|  > Digite sua pergunta sobre o orçamento...                           |
|_______________________________________________________________________|
```
```
