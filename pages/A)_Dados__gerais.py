import streamlit as st
from dataset import df_categ_geral, df_geral_cadunico
from graficos import plot_zscore_brasil, plot_grafico_geral

st.set_page_config(page_title="📊 Geral", layout="wide")

# Filtros na sidebar
sexo_opcao = st.sidebar.radio("Sexo:", ["Masculino", "Feminino"])
reg_cadunico_opcao = st.sidebar.radio("Região Cadastral:", ["Rural", "Urbana"])

df_kpi = df_categ_geral.query(
    "sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
)

#st.caption(f"Filtros - Sexo: {sexo_opcao} | Região: {reg_cadunico_opcao}")
st.markdown(
    f"""
    <div style='text-align: right; color: gray; margin-top: -30px;'>
        Filtros - Sexo: {sexo_opcao} | Região: {reg_cadunico_opcao}
    </div>
    """,
    unsafe_allow_html=True
)


# Cria duas colunas
col1, col2 = st.columns([0.4,0.6])

# Gráfico Geral na Coluna 1
with col1:
    fig = plot_grafico_geral(df_geral_cadunico, ["med_altura", "med_peso", "med_imc"])
    fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=300)
    st.plotly_chart(fig, use_container_width=True)

# Gráfico Z-Score na Coluna 2
with col2:    

    fig = plot_zscore_brasil(df_kpi)
    fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=300)
    st.plotly_chart(fig, use_container_width=True)
