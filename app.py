import pandas as pd
import streamlit as st

from dataset import (
    df_categ_geral, 
    df_categ_raca, 
    df_categ_regiao, 
    df_categ_estados, 
    #df_categorias_prevalencia,
    df_categ_estados_prev
)
from graficos import plot_zscore_brasil, plot_zscore_por_regiao, plot_zscore_por_estado, gerar_grafico_imc_altura, gerar_grafico_radial_obesidade

# ----------------- CONFIGURAÇÕES INICIAIS ----------------- #
st.set_page_config(page_title="Gráficos de Saúde Infantil", layout="wide")
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3, h4, h5 {
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Indicadores de Saúde Infantil")

# ----------------- MAPEAMENTO E AJUSTES ----------------- #
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

# ----------------- FUNÇÃO: TÍTULO COM ESTILO ----------------- #
def styled_title(text, level=5):
    return f"<h{level} style='margin-bottom: 5px; color:#2c3e50'>{text}</h{level}>"

# ----------------- SIDEBAR - FILTROS ----------------- #
with st.sidebar.expander("🎛️ Filtros", expanded=True):
    sexo_opcao = st.radio("Sexo:", ["Masculino", "Feminino"])
    reg_cadunico_opcao = st.radio("Região Cadastral:", ["Rural", "Urbana"])
    categoria_opcao = st.selectbox("Raça:", df_categ_raca["categoria"].unique())
    regiao_opcao = st.multiselect("Região:", df_categ_regiao["categoria"].unique())
    estados_opcao = st.multiselect("Estados:", df_categ_estados["categoria"].unique())
    idade_opcao = st.selectbox("Idade:", df_categ_estados_prev["idade_cat"].unique())
    

# ----------------- TABS ----------------- #
aba_geral, aba_raca, aba_regiao, aba_estado, aba_radial = st.tabs([
    "📊 Brasil Geral", "🎯 Por Raça", "🌍 Por Região", "🏙️ Por Estado", "📌 Prevalência de Obesidade"
])

# ----------------- ABA 1: GERAL ----------------- #
with aba_geral:
    df_kpi = df_categ_geral.query("sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao")
    st.markdown(styled_title(f"Brasil - Sexo: {sexo_opcao} | Região: {reg_cadunico_opcao}"), unsafe_allow_html=True)
    plot_zscore_brasil(df_kpi)

# ----------------- ABA 2: RAÇA ----------------- #
with aba_raca:
    df_raca = df_categ_raca.query("sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao and categoria == @categoria_opcao")
    st.markdown(styled_title(f"Raça: {categoria_opcao} | Sexo: {sexo_opcao} | Região: {reg_cadunico_opcao}"), unsafe_allow_html=True)
    plot_zscore_brasil(df_raca)

# ----------------- ABA 3: REGIÃO ----------------- #
with aba_regiao:
    df_regiao = df_categ_regiao.query("sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao")
    if regiao_opcao:
        df_regiao = df_regiao[df_regiao["categoria"].isin(regiao_opcao)]
    regioes_str = ", ".join(regiao_opcao) if regiao_opcao else "Todas"

    st.markdown(styled_title(f"Z-Score por Região - Sexo: {sexo_opcao} | Região Cadastral: {reg_cadunico_opcao} | Regiões: {regioes_str}"), unsafe_allow_html=True)

    #st.markdown("<h6 style='text-align:center;'>IMC</h6>", unsafe_allow_html=True)
    plot_zscore_por_regiao(df_regiao, 'med_imc')

    st.divider()

    #col1, col2 = st.columns(2)
    #with col1:
    #st.markdown("<h6 style='text-align:center;'>Peso</h6>", unsafe_allow_html=True)
    plot_zscore_por_regiao(df_regiao, 'med_peso')
    #with col2:
    #st.markdown("<h6 style='text-align:center;'>Altura</h6>", unsafe_allow_html=True)
    plot_zscore_por_regiao(df_regiao, 'med_altura')

# ----------------- ABA 4: ESTADOS ----------------- #
with aba_estado:
    df_estados = df_categ_estados.query("sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao")
    if regiao_opcao:
        df_estados = df_estados[df_estados["regiao"].isin(regiao_opcao)]
    if estados_opcao:
        df_estados = df_estados[df_estados["categoria"].isin(estados_opcao)]

    regioes_str = ", ".join(regiao_opcao) if regiao_opcao else "Todas"
    estados_str = ", ".join(estados_opcao) if estados_opcao else "Todos"

    st.markdown(styled_title(f"Z-Score por Estado - Sexo: {sexo_opcao} | Região Cadastral: {reg_cadunico_opcao} | Regiões: {regioes_str} | Estados: {estados_str}"), unsafe_allow_html=True)

    #st.markdown("<h6 style='text-align:center;'>IMC</h6>", unsafe_allow_html=True)
    plot_zscore_por_estado(df_estados, 'med_imc')

    st.divider()

    #col1, col2 = st.columns(2)
    #with col1:
    #st.markdown("<h6 style='text-align:center;'>Peso</h6>", unsafe_allow_html=True)
    plot_zscore_por_estado(df_estados, 'med_peso')
    #with col2:
    #st.markdown("<h6 style='text-align:center;'>Altura</h6>", unsafe_allow_html=True)
    plot_zscore_por_estado(df_estados, 'med_altura')

# ----------------- ABA 5: GRÁFICO RADIAL ----------------- #
with aba_radial:
    df_categ_estados_prev["regiao"] = df_categ_estados_prev["categoria"].map(estados_para_regiao)

    df_estados_prev = df_categ_estados_prev.query("idade_cat == @idade_opcao and sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao")
    if regiao_opcao:
        df_estados_prev = df_estados_prev[df_estados_prev["regiao"].isin(regiao_opcao)]
    if estados_opcao:
        df_estados_prev = df_estados_prev[df_estados_prev["categoria"].isin(estados_opcao)]

    st.markdown(styled_title(f"Prevalência de Obesidade (Idade: {idade_opcao}, {sexo_opcao}, {reg_cadunico_opcao})"), unsafe_allow_html=True)
    gerar_grafico_radial_obesidade(df_estados_prev)    