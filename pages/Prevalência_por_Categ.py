import streamlit as st
from dataset import (
    df_categ_geral_prev, df_categ_regiao_prev,
    df_categ_estados_prev, df_categ_raca_prev
)
from graficos import (
    gerar_pizza_composicao_peso, gerar_grafico_radial_obesidade
)

# ----------------- MAPEAMENTO ----------------- #
estados_para_regiao = {
    "Acre": "norte", "Alagoas": "nordeste", "Amapa": "norte", "Amazonas": "norte",
    "Bahia": "nordeste", "Ceara": "nordeste", "Distrito Federal": "centro_oeste",
    "Espirito Santo": "sudeste", "Goias": "centro_oeste", "Maranhao": "nordeste",
    "Mato Grosso": "centro_oeste", "Mato Grosso do Sul": "centro_oeste", "Minas Gerais": "sudeste",
    "Para": "norte", "Paraiba": "nordeste", "Parana": "sul", "Pernambuco": "nordeste",
    "Piaui": "nordeste", "Rio de Janeiro": "sudeste", "Rio Grande do norte": "nordeste",
    "Rio Grande do Sul": "sul", "Rondonia": "norte", "Roraima": "norte", "Santa Catarina": "sul",
    "Sao Paulo": "sudeste", "Sergipe": "nordeste", "Tocantins": "norte", "Rio Grande do Norte": "nordeste",
}
df_categ_estados_prev["regiao"] = df_categ_estados_prev["categoria"].map(estados_para_regiao)

st.set_page_config(page_title="📌 Prevalência de Obesidade", layout="wide")

sexo_opcao = st.sidebar.radio("Sexo:", ["Masculino", "Feminino"])
reg_cadunico_opcao = st.sidebar.radio("Região Cadastral:", ["Rural", "Urbana"])
idade_opcao = st.sidebar.selectbox("Idade:", df_categ_estados_prev["idade_cat"].unique())
regiao_opcao = st.sidebar.multiselect("Região:", df_categ_regiao_prev["categoria"].unique())
estados_opcao = st.sidebar.multiselect("Estados:", df_categ_estados_prev["categoria"].unique())

abas = st.tabs(["📊 Composição Geral", "📍 Por Região", "🗺️ Por Estado", "🌎 Por Raça"])

# Geral
with abas[0]:
    df = df_categ_geral_prev.query(
        "idade_cat == @idade_opcao and sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
    )
    st.caption(f"Filtros: Idade {idade_opcao}, Sexo {sexo_opcao}, Região {reg_cadunico_opcao}")
    gerar_pizza_composicao_peso(df)

# Por Região
with abas[1]:
    df = df_categ_regiao_prev.query(
        "idade_cat == @idade_opcao and sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
    )
    if regiao_opcao:
        df = df[df["categoria"].isin(regiao_opcao)]
        regiao = regiao_opcao
    else:
        regiao = "Todas"

    st.caption(f"Filtros: Idade {idade_opcao}, Sexo {sexo_opcao}, Região {reg_cadunico_opcao} | {regiao}")
    gerar_grafico_radial_obesidade(df, modo='regiao')

# Por Estado
with abas[2]:
    df = df_categ_estados_prev.query(
        "idade_cat == @idade_opcao and sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
    )
    if regiao_opcao:
        df = df[df["regiao"].isin(regiao_opcao)]
        regiao = regiao_opcao
    else:
        regiao = "Todas"

    if estados_opcao:
        df = df[df["categoria"].isin(estados_opcao)]
        estado = estados_opcao
    else:
        estado = "Todos"

    st.caption(f"Filtros: Idade {idade_opcao}, Sexo {sexo_opcao}, Região {reg_cadunico_opcao} | {regiao} | {estado}")
    gerar_grafico_radial_obesidade(df, modo='estado')

# Por Raça
with abas[3]:
    df = df_categ_raca_prev.query(
        "idade_cat == @idade_opcao and sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
    )
    st.caption(f"Filtros: Idade {idade_opcao}, Sexo {sexo_opcao}, Região {reg_cadunico_opcao}")
    gerar_grafico_radial_obesidade(df, modo='raca')
