import streamlit as st
from dataset import df_categ_regiao,df_geral_regiao
from graficos import plot_zscore_por_regiao,plot_grafico_geral_por_regiao
import pandas as pd

st.set_page_config(page_title="🌍 Por Região", layout="wide")

sexo_opcao = st.sidebar.radio("Sexo:", ["Masculino", "Feminino"])
reg_cadunico_opcao = st.sidebar.radio("Região Cadastral:", ["Rural", "Urbana"])

# INICIO: Código incluido para mostrar labels amigáveis na sidebar
# Mapeamento: original -> label
mapa_labels = {
    "centro_oeste": "Centro Oeste",
    "sudeste": "Sudeste",
    "nordeste": "Nordeste",
    "norte": "Norte",
    "sul": "Sul"
}

# Criar lista de labels na mesma ordem do dataframe
labels = [mapa_labels[val] for val in df_categ_regiao["categoria"].unique()]

# Mostra os labels, mas seleciona retorna em labels
labels_escolhidos = st.sidebar.multiselect("Região:", labels)

# Traduz de volta para os valores originais
regiao_opcao = [orig for orig, label in mapa_labels.items() if label in labels_escolhidos]

#regiao_opcao = st.sidebar.multiselect("Região:", df_categ_regiao["categoria"].unique())

# FIM: Código incluido para mostrar labels amigáveis na sidebar

df_regiao = df_categ_regiao.query(
    "sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
)

if regiao_opcao:
    df_regiao = df_regiao[df_regiao["categoria"].isin(regiao_opcao)]
    df_geral_regiao = df_geral_regiao[df_geral_regiao["categoria"].isin(regiao_opcao)]


regioes_str = ", ".join(regiao_opcao) if regiao_opcao else "Todas"

st.caption(f"Filtros - Sexo: {sexo_opcao} | {reg_cadunico_opcao} | Regiões: {regioes_str}")

df_geral_regiao = df_geral_regiao.query(
    "sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
)

# # Gerar e exibir o gráfico
plot_grafico_geral_por_regiao(df_geral_regiao)
st.divider()
plot_zscore_por_regiao(df_regiao, 'med_imc')
st.divider()
plot_zscore_por_regiao(df_regiao, 'med_peso')
st.divider()
plot_zscore_por_regiao(df_regiao, 'med_altura')

