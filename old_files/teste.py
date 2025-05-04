import pandas as pd
import streamlit as st

from dataset import df_categ_geral, df_categ_raca, df_categ_regiao, df_categ_estados,df_categorias_prevalencia
from graficos import plot_zscore_brasil, plot_zscore_por_regiao, plot_zscore_por_estado,gerar_grafico_imc_altura,gerar_grafico_radial_obesidade

# ----------------- CONFIGURAÇÕES INICIAIS ----------------- #
st.set_page_config(page_title="Gráficos de Saúde Infantil", layout="wide")
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
    "Sao Paulo": "sudeste", "Sergipe": "nordeste", "Tocantins": "norte","Rio Grande do Norte": "nordeste",
}

df_categ_estados["regiao"] = df_categ_estados["categoria"].map(estados_para_regiao)

# ----------------- FUNÇÃO: TÍTULO COM ESTILO ----------------- #
def styled_title(text, level=5):
    return f"<h{level} style='margin-bottom: 5px; color:#2c3e50'>{text}</h{level}>"

# ----------------- SIDEBAR - FILTROS ----------------- #
with st.sidebar.expander("🎛️ Filtros", expanded=True):
    sexo_opcao = st.selectbox("Sexo:", ["Masculino", "Feminino"])
    reg_cadunico_opcao = st.selectbox("Região Cadastral:", ["Rural", "Urbana"])
    categoria_opcao = st.selectbox("Raça:", df_categ_raca["categoria"].unique())
    regiao_opcao = st.multiselect("Região:", df_categ_regiao["categoria"].unique())
    estados_opcao = st.multiselect("Estados:", df_categ_estados["categoria"].unique())

# ----------------- GRÁFICO GERAL BRASIL ----------------- #
col1, col2 = st.columns(2)

with col1:
    st.markdown(styled_title(f"Brasil - Sexo: {sexo_opcao} | Região: {reg_cadunico_opcao}"), unsafe_allow_html=True)
    df_geral = df_categ_geral.query("sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao")
    plot_zscore_brasil(df_geral)

# ----------------- GRÁFICO POR RAÇA ----------------- #
with col2:
    st.markdown(styled_title(f"Raça: {categoria_opcao} | Sexo: {sexo_opcao} | Região: {reg_cadunico_opcao}"), unsafe_allow_html=True)
    df_raca = df_categ_raca.query("sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao and categoria == @categoria_opcao")
    plot_zscore_brasil(df_raca)

# ----------------- GRÁFICO POR REGIÃO ----------------- #
df_regiao = df_categ_regiao.query(
    "sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao" +
    (" and categoria in @regiao_opcao" if regiao_opcao else "")
)

regioes_str = ", ".join(regiao_opcao) if regiao_opcao else "Todas"
st.markdown(styled_title(f"Z-Score Idade x Região - Sexo: {sexo_opcao} | Região Cadastral: {reg_cadunico_opcao} | Região: {regioes_str}"), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<h6 style='text-align:center;'>Peso</h6>", unsafe_allow_html=True)
    plot_zscore_por_regiao(df_regiao, 'med_peso')

with col2:
    st.markdown("<h6 style='text-align:center;'>Altura</h6>", unsafe_allow_html=True)
    plot_zscore_por_regiao(df_regiao, 'med_altura')

with col3:
    st.markdown("<h6 style='text-align:center;'>IMC</h6>", unsafe_allow_html=True)
    plot_zscore_por_regiao(df_regiao, 'med_imc')

# ----------------- GRÁFICO POR ESTADO ----------------- #
df_estados = df_categ_estados.query(
    "sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
)
if regiao_opcao:
    df_estados = df_estados[df_estados["regiao"].isin(regiao_opcao)]
if estados_opcao:
    df_estados = df_estados[df_estados["categoria"].isin(estados_opcao)]

estados_str = ", ".join(estados_opcao) if estados_opcao else "Todos"

st.markdown(styled_title(f"Z-Score Idade x Estado - Sexo: {sexo_opcao} | Região Cadastral: {reg_cadunico_opcao} | Região: {regioes_str} | Estado: {estados_str}"), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<h6 style='text-align:center;'>Peso</h6>", unsafe_allow_html=True)
    plot_zscore_por_estado(df_estados, 'med_peso')

with col2:
    st.markdown("<h6 style='text-align:center;'>Altura</h6>", unsafe_allow_html=True)
    plot_zscore_por_estado(df_estados, 'med_altura')

with col3:
    st.markdown("<h6 style='text-align:center;'>IMC</h6>", unsafe_allow_html=True)
    plot_zscore_por_estado(df_estados, 'med_imc')


df = df_categorias_prevalencia.query('tabela == "estados" '
                                        'and idade_cat == "5a"' \
                                        'and sexo=="Feminino" ' \
                                        'and region_cadunico=="Urbana"').copy()

df["regiao"] = df["categoria"].map(estados_para_regiao)

gerar_grafico_radial_obesidade(df)

