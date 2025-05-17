import streamlit as st
from dataset import df_categ_estados
from graficos import plot_zscore_por_estado

st.set_page_config(page_title="🏙️ Por Estado", layout="wide")

# Mapeamento necessário para adicionar a coluna de região
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
df_categ_estados["regiao"] = df_categ_estados["categoria"].map(estados_para_regiao)

sexo_opcao = st.sidebar.radio("Sexo:", ["Masculino", "Feminino"])
reg_cadunico_opcao = st.sidebar.radio("Região Cadastral:", ["Rural", "Urbana"])
regiao_opcao = st.sidebar.multiselect("Região:", df_categ_estados["regiao"].dropna().unique())
estados_opcao = st.sidebar.multiselect("Estados:", df_categ_estados["categoria"].unique())

df_estados = df_categ_estados.query(
    "sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
)

if regiao_opcao:
    df_estados = df_estados[df_estados["regiao"].isin(regiao_opcao)]
if estados_opcao:
    df_estados = df_estados[df_estados["categoria"].isin(estados_opcao)]

regioes_str = ", ".join(regiao_opcao) if regiao_opcao else "Todas"
estados_str = ", ".join(estados_opcao) if estados_opcao else "Todos"

st.caption(f"Filtros - Sexo: {sexo_opcao} | {reg_cadunico_opcao} | Regiões: {regioes_str} | Estados: {estados_str}")

plot_zscore_por_estado(df_estados, 'med_imc')
st.divider()
plot_zscore_por_estado(df_estados, 'med_peso')
st.divider()
plot_zscore_por_estado(df_estados, 'med_altura')
