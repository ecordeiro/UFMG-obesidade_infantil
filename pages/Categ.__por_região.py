import streamlit as st
from dataset import df_categ_regiao
from graficos import plot_zscore_por_regiao

st.set_page_config(page_title="🌍 Por Região", layout="wide")

sexo_opcao = st.sidebar.radio("Sexo:", ["Masculino", "Feminino"])
reg_cadunico_opcao = st.sidebar.radio("Região Cadastral:", ["Rural", "Urbana"])
regiao_opcao = st.sidebar.multiselect("Região:", df_categ_regiao["categoria"].unique())

df_regiao = df_categ_regiao.query(
    "sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
)

if regiao_opcao:
    df_regiao = df_regiao[df_regiao["categoria"].isin(regiao_opcao)]

regioes_str = ", ".join(regiao_opcao) if regiao_opcao else "Todas"

st.caption(f"Filtros - Sexo: {sexo_opcao} | {reg_cadunico_opcao} | Regiões: {regioes_str}")

plot_zscore_por_regiao(df_regiao, 'med_imc')
st.divider()
plot_zscore_por_regiao(df_regiao, 'med_peso')
plot_zscore_por_regiao(df_regiao, 'med_altura')
