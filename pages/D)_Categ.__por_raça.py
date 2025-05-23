import streamlit as st
from dataset import df_categ_raca
from graficos import plot_zscore_brasil

st.set_page_config(page_title="🎯 Por Raça", layout="wide")

sexo_opcao = st.sidebar.radio("Sexo:", ["Masculino", "Feminino"])
reg_cadunico_opcao = st.sidebar.radio("Região Cadastral:", ["Rural", "Urbana"])
categoria_opcao = st.sidebar.selectbox("Raça:", df_categ_raca["categoria"].unique())

df_raca = df_categ_raca.query(
    "sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao and categoria == @categoria_opcao"
)

st.caption(f"Filtros: Raça: {categoria_opcao} | Sexo: {sexo_opcao} | Região: {reg_cadunico_opcao}")
#plot_zscore_brasil(df_raca)
fig = plot_zscore_brasil(df_raca)
fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=300)
st.plotly_chart(fig, use_container_width=True)
