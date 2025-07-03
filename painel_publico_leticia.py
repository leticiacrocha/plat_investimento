
import streamlit as st
import yfinance as yf
import requests
import pandas as pd

st.set_page_config(page_title="Painel de Investimentos - Letícia", layout="wide")
st.title("📊 Painel de Investimentos Automatizado - Versão Pública")
st.markdown("Ativos de risco médio e baixo aporte, atualizados automaticamente via APIs gratuitas.")

# --- Função: buscar cotação de ETFs e ações ---
def buscar_ativos_yfinance(tickers):
    ativos = []
    for ticker in tickers:
        dados = yf.Ticker(ticker)
        hist = dados.history(period="7d")
        preco = hist["Close"][-1] if not hist.empty else None
        ativos.append({
            "Ativo": ticker,
            "Categoria": "ETF/Ação",
            "Preço Atual (R$)": round(preco, 2) if preco else "N/D",
            "Fonte": "Yahoo Finance"
        })
    return ativos

# --- Função: buscar criptos via CoinGecko ---
def buscar_criptos(ids):
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ",".join(ids), "vs_currencies": "brl"}
    resposta = requests.get(url, params=params)
    precos = resposta.json()
    cripto_data = []
    for id_cripto in ids:
        preco = precos.get(id_cripto, {}).get("brl", None)
        cripto_data.append({
            "Ativo": id_cripto.upper(),
            "Categoria": "Criptomoeda",
            "Preço Atual (R$)": round(preco, 2) if preco else "N/D",
            "Fonte": "CoinGecko"
        })
    return cripto_data

# --- Coletar dados ---
tickers_b3 = ["BOVA11.SA", "IVVB11.SA", "SMAL11.SA", "ITUB4.SA"]
criptos = ["bitcoin", "ethereum", "usd-coin"]
dados_ativos = buscar_ativos_yfinance(tickers_b3) + buscar_criptos(criptos)

df = pd.DataFrame(dados_ativos)

# --- Filtros ---
categoria = st.sidebar.multiselect("Filtrar por categoria", df["Categoria"].unique(), default=df["Categoria"].unique())
df_filtrado = df[df["Categoria"].isin(categoria)]

# --- Exibir tabela ---
st.subheader("📈 Ativos recomendados")
st.dataframe(df_filtrado, use_container_width=True)

# --- Simulador de aporte ---
st.markdown("---")
st.subheader("📝 Registrar Aporte (simulação)")
opcao = st.selectbox("Escolha o ativo", df_filtrado["Ativo"].unique())
valor = st.number_input("Valor do aporte (R$)", min_value=10.0, step=10.0)
if st.button("Registrar Aporte"):
    st.success(f"Aporte registrado em {opcao} no valor de R${valor:.2f}")
