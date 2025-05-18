import streamlit as st
from dataset import df_categ_geral
from dataset import df_geral_geral
from graficos import plot_zscore_brasil, plot_grafico_geral

st.set_page_config(page_title="📊 Geral", layout="wide")

# Gera o gráfico geral e aplica menos margem
fig = plot_grafico_geral(df_geral_geral, ["med_altura", "med_peso", "med_imc"])
fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=280)
st.plotly_chart(fig, use_container_width=True)

# Diminui o espaço entre os dois gráficos
st.markdown('<div style="margin-top:-30px;"></div>', unsafe_allow_html=True)

# Filtros
sexo_opcao = st.sidebar.radio("Sexo:", ["Masculino", "Feminino"])
reg_cadunico_opcao = st.sidebar.radio("Região Cadastral:", ["Rural", "Urbana"])

df_kpi = df_categ_geral.query(
    "sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
)

st.caption(f"Filtros - Sexo: {sexo_opcao} | Região: {reg_cadunico_opcao}")

# Gráfico por idade
plot_zscore_brasil(df_kpi)
