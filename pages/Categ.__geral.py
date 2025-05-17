import streamlit as st
from dataset import df_categ_geral
from graficos import plot_zscore_brasil

st.set_page_config(page_title="📊 Categoria - Geral", layout="wide")

#st.title("📊 Brasil Geral")

sexo_opcao = st.sidebar.radio("Sexo:", ["Masculino", "Feminino"])
reg_cadunico_opcao = st.sidebar.radio("Região Cadastral:", ["Rural", "Urbana"])

df_kpi = df_categ_geral.query(
    "sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
)

st.subheader(f"Brasil - Sexo: {sexo_opcao} | Região: {reg_cadunico_opcao}")
plot_zscore_brasil(df_kpi)
