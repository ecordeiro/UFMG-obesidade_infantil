import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from dataset import (
    df_categ_estados_prev
)

# --- Título
#st.title("Heatmap da Prevalência por Estado")
#st.markdown("Selecione o sexo e a região para visualizar o mapa de prevalência.")

# --- Carregar dados
@st.cache_data
def carregar_dados():
    df = df_categ_estados_prev.copy()
    return df

df = carregar_dados()

# --- Filtros interativos
sexo_opcao = st.sidebar.selectbox("Sexo:", sorted(df["sexo"].unique()))
regiao_opcao = st.sidebar.selectbox("Região (CadÚnico):", sorted(df["region_cadunico"].unique()))

# --- Filtrar dados
df_filtrado = df[(df["sexo"] == sexo_opcao) & (df["region_cadunico"] == regiao_opcao)]

# --- Renomear coluna 'categoria' para 'estado'
df_filtrado = df_filtrado.rename(columns={"categoria": "estado"})

# Corrigir nomes de estados sem acento
correcao_estados = {
    "Amapa": "Amapá",
    "Ceara": "Ceará",
    "Rondonia": "Rondônia",
    "Espirito Santo": "Espírito Santo",
    "Maranhao": "Maranhão",
    "Goias": "Goiás", 
    "Para": "Pará", 
    "Parana": "Paraná", 
    "Paraiba": "Paraíba",
    "Piaui": "Piauí",
    "Sao Paulo": "São Paulo"
}

df_filtrado["estado"] = df_filtrado["estado"].replace(correcao_estados)

# --- GeoJSON dos estados brasileiros
geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
geojson = requests.get(geojson_url).json()

# --- Heatmap (pode alternar entre 'prev_obesidade' e 'prev_excesso')
coluna_valor = st.sidebar.radio("Indicador:", ["prev_obesidade", "prev_excesso"])

fig = px.choropleth(
    df_filtrado,
    geojson=geojson,
    locations="estado",
    color=coluna_valor,
    featureidkey="properties.name",
    color_continuous_scale="Reds",
    scope="south america",
    # labels={
    #     "prev_obesidade": "Obesidade (%)",
    #     "prev_excesso": "Excesso de Peso (%)"
    # },
    labels={
        "estado": "Estado",
        "prev_obesidade": "Obesidade (%)",
        "prev_excesso": "Excesso de Peso (%)"
    },
    title=f"{'Obesidade' if coluna_valor == 'prev_obesidade' else 'Excesso de Peso'} por Estado | {sexo_opcao} |{regiao_opcao}",
    hover_name="estado"
)

fig.update_geos(fitbounds="locations", visible=False)

# 👉 Aqui entra a customização do fundo transparente
fig.update_layout(
    autosize=True,
    width=1000,   # largura em pixels
    height=500,   # altura em pixels
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    geo=dict(bgcolor='rgba(0,0,0,0)'),
    font_color="white",  # só se você quiser manter contraste no dark mode
    margin=dict(t=25, l=0, r=0, b=0)
)

st.plotly_chart(fig, use_container_width=True)
