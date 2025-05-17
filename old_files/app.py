import pandas as pd
import streamlit as st

from dataset import (
    df_categ_geral, 
    df_categ_raca, 
    df_categ_regiao, 
    df_categ_estados, 
    df_categ_estados_prev,
    df_categ_geral_prev,
    df_categ_regiao_prev,
    df_categ_raca_prev,
)

from graficos import (
    plot_zscore_brasil, 
    plot_zscore_por_regiao, 
    plot_zscore_por_estado,     
    gerar_grafico_radial_obesidade,    
    gerar_pizza_composicao_peso
)

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

st.markdown(
    "<h4 style='text-align: left; color: white;'>📊 Indicadores Antropométricos de Crescimento Infantil</h4>",
    unsafe_allow_html=True
)

st.markdown("""
    <style>
    /* Reduz tudo dentro da sidebar */
    [data-testid="stSidebar"] * {
        font-size: 0.75rem !important;
        font-weight: 300 !important;
    }

    [data-testid="stSidebar"] .block-container {
        padding: 1rem;
    }

    [data-testid="stSidebar"] .stRadio, 
    [data-testid="stSidebar"] .stSelectbox, 
    [data-testid="stSidebar"] .stMultiSelect {
        margin-bottom: 0.5rem;
    }

    /* Reduz fontes do menu dropdown (fora da sidebar) */
    div[role="listbox"] > div {
        font-size: 0.75rem !important;
    }

    /* Também reduz o texto selecionado dentro do select */
    .css-1pahdxg-control, .css-1dimb5e-singleValue {
        font-size: 0.75rem !important;
    }

    /* Reduz o botão de seta e outras partes internas */
    .css-319lph-ValueContainer, .css-tlfecz-indicatorContainer {
        font-size: 0.75rem !important;
    }
    </style>
""", unsafe_allow_html=True)



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
df_categ_estados["regiao"] = df_categ_estados["categoria"].map(estados_para_regiao)
df_categ_estados_prev["regiao"] = df_categ_estados_prev["categoria"].map(estados_para_regiao)

# ----------------- FUNÇÃO: TÍTULO COM ESTILO ----------------- #
def styled_title(text, level=5):
    return f"<h{level} style='margin-bottom: 5px; color:#2c3e50'>{text}</h{level}>"

# ----------------- CONTROLE DE ABA ATIVA ----------------- #
aba_ativa = st.sidebar.radio("Navegação", [
    "📊 Brasil Geral", 
    "🎯 Por Raça", 
    "🌍 Por Região", 
    "🏙️ Por Estado", 
    "📌 Prevalência de Obesidade"
])

# ----------------- FILTROS COMUNS ----------------- #
sexo_opcao = st.sidebar.radio("Sexo:", ["Masculino", "Feminino"])
reg_cadunico_opcao = st.sidebar.radio("Região Cadastral:", ["Rural", "Urbana"])

# ----------------- FILTROS ESPECÍFICOS ----------------- #
categoria_opcao = None
regiao_opcao = []
estados_opcao = []

if aba_ativa == "🎯 Por Raça":
    categoria_opcao = st.sidebar.selectbox("Raça:", df_categ_raca["categoria"].unique())

if aba_ativa in ["🌍 Por Região", "🏙️ Por Estado"]:
    regiao_opcao = st.sidebar.multiselect("Região:", df_categ_regiao["categoria"].unique())

if aba_ativa in ["🏙️ Por Estado"]:
    estados_opcao = st.sidebar.multiselect("Estados:", df_categ_estados["categoria"].unique())    

if aba_ativa in ["📌 Prevalência de Obesidade"]:
    idade_opcao = st.sidebar.selectbox("Idade:", df_categ_estados_prev["idade_cat"].unique())
    regiao_opcao = st.sidebar.multiselect("Região:", df_categ_regiao["categoria"].unique())    
    estados_opcao = st.sidebar.multiselect("Estados:", df_categ_estados["categoria"].unique())
    

# ----------------- CONTEÚDO DE CADA ABA ----------------- #

# 📊 Brasil Geral
if aba_ativa == "📊 Brasil Geral":
    df_kpi = df_categ_geral.query("sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao")
    st.markdown(styled_title(f"Brasil - Sexo: {sexo_opcao} | Região: {reg_cadunico_opcao}"), unsafe_allow_html=True)
    plot_zscore_brasil(df_kpi)

# 🎯 Por Raça
elif aba_ativa == "🎯 Por Raça":
    df_raca = df_categ_raca.query("sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao and categoria == @categoria_opcao")
    st.markdown(styled_title(f"Raça: {categoria_opcao} | Sexo: {sexo_opcao} | Região: {reg_cadunico_opcao}"), unsafe_allow_html=True)
    plot_zscore_brasil(df_raca)

# 🌍 Por Região
elif aba_ativa == "🌍 Por Região":
    df_regiao = df_categ_regiao.query("sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao")
    if regiao_opcao:
        df_regiao = df_regiao[df_regiao["categoria"].isin(regiao_opcao)]

    regioes_str = ", ".join(regiao_opcao) if regiao_opcao else "Todas"
    st.markdown(styled_title(f"Z-Score por Região - Sexo: {sexo_opcao} | {reg_cadunico_opcao} | Regiões: {regioes_str}"), unsafe_allow_html=True)
    plot_zscore_por_regiao(df_regiao, 'med_imc')
    st.divider()
    plot_zscore_por_regiao(df_regiao, 'med_peso')
    plot_zscore_por_regiao(df_regiao, 'med_altura')

# 🏙️ Por Estado
elif aba_ativa == "🏙️ Por Estado":
    df_estados = df_categ_estados.query("sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao")
    if regiao_opcao:
        df_estados = df_estados[df_estados["regiao"].isin(regiao_opcao)]
    if estados_opcao:
        df_estados = df_estados[df_estados["categoria"].isin(estados_opcao)]

    regioes_str = ", ".join(regiao_opcao) if regiao_opcao else "Todas"
    estados_str = ", ".join(estados_opcao) if estados_opcao else "Todos"
    st.markdown(styled_title(f"Z-Score por Estado - Sexo: {sexo_opcao} | {reg_cadunico_opcao} | Regiões: {regioes_str} | Estados: {estados_str}"), unsafe_allow_html=True)
    plot_zscore_por_estado(df_estados, 'med_imc')
    st.divider()
    plot_zscore_por_estado(df_estados, 'med_peso')
    plot_zscore_por_estado(df_estados, 'med_altura')
    

# 📌 Prevalência de Obesidade
elif aba_ativa == "📌 Prevalência de Obesidade":

    abas = st.tabs(["📊 Composição Geral", "📍 Por Região", "🗺️ Por Estado", "🌎 Por Raça"])

    #Dados Gerais    
    with abas[0]:

        df_categ_geral_prev = df_categ_geral_prev.query(
            "idade_cat == @idade_opcao and sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
        )

        st.markdown(styled_title(f"Filtros (Idade: {idade_opcao}, {sexo_opcao}, {reg_cadunico_opcao})"), unsafe_allow_html=True)

        gerar_pizza_composicao_peso(df_categ_geral_prev)

    #Dados por Regiao
    with abas[1]:
    

        if regiao_opcao:
            df_categ_regiao_prev = df_categ_regiao_prev[df_categ_regiao_prev["categoria"].isin(regiao_opcao)]
            regiao=regiao_opcao
        else:
            regiao="Todas"

        df_categ_regiao_prev = df_categ_regiao_prev.query(
            "idade_cat == @idade_opcao and sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
        )

        st.markdown(styled_title(f"Filtros (Idade: {idade_opcao}, {sexo_opcao}, {reg_cadunico_opcao}| {regiao})"), unsafe_allow_html=True)    
        gerar_grafico_radial_obesidade(df_categ_regiao_prev, modo='regiao')

    #Dados por Estado
    with abas[2]:        

        df_estados_prev = df_categ_estados_prev.query(
            "idade_cat == @idade_opcao and sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
        )
        if regiao_opcao:
            df_estados_prev = df_estados_prev[df_estados_prev["regiao"].isin(regiao_opcao)]
            regiao=regiao_opcao
        else:
            regiao="Todas"

        if estados_opcao:
            df_estados_prev = df_estados_prev[df_estados_prev["categoria"].isin(estados_opcao)]
            estado = estados_opcao
        else:
            estado = "Todos"    

        st.markdown(styled_title(f"Filtros (Idade: {idade_opcao}, {sexo_opcao}, {reg_cadunico_opcao}| {regiao} | {estado})"), unsafe_allow_html=True)    
        gerar_grafico_radial_obesidade(df_estados_prev, modo='estado')

    #Dados por Raça    
    with abas[3]:        

        df_categ_raca_prev = df_categ_raca_prev.query(
            "idade_cat == @idade_opcao and sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
        )

        st.markdown(styled_title(f"Filtros (Idade: {idade_opcao}, {sexo_opcao}, {reg_cadunico_opcao})"), unsafe_allow_html=True)    
        gerar_grafico_radial_obesidade(df_categ_raca_prev, modo='raca')

    