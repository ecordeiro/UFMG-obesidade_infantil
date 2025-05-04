import pandas as pd
from dataset import df_categ_geral
from dataset import df_categ_raca
from dataset import df_categ_regiao
from dataset import df_categ_estados
import streamlit as st
from graficos import plot_zscore_brasil,plot_zscore_por_regiao, plot_zscore_por_estado

estados_para_regiao = {
    "Acre": "norte", "Alagoas": "nordeste", "Amapá": "norte", "Amazonas": "norte",
    "Bahia": "nordeste", "Ceará": "nordeste", "Distrito Federal": "centro_oeste",
    "Espírito Santo": "sudeste", "Goiás": "centro_oeste", "Maranhão": "nordeste",
    "Mato Grosso": "centro_oeste", "Mato Grosso do Sul": "centro_oeste", "Minas Gerais": "sudeste",
    "Pará": "norte", "Paraíba": "nordeste", "Paraná": "sul", "Pernambuco": "nordeste",
    "Piauí": "nordeste", "Rio de Janeiro": "sudeste", "Rio Grande do norte": "nordeste",
    "Rio Grande do Sul": "sul", "Rondônia": "norte", "Roraima": "norte", "Santa Catarina": "sul",
    "São Paulo": "sudeste", "Sergipe": "nordeste", "Tocantins": "norte"
}

df_categ_estados["regiao"] = df_categ_estados["categoria"].map(estados_para_regiao)


# Define layout como wide
st.set_page_config(page_title="Gráficos de Saúde Infantil", layout="wide")

st.title("Indicadores de Saúde Infantil")

#---------------------------FILTROS -----------------------------
# Filtros na barra lateral
st.sidebar.header("Filtros")

sexo_opcao = st.sidebar.selectbox("Sexo:", ["Masculino", "Feminino"])

reg_cadunico_opcao = st.sidebar.selectbox("Região Cadastral:", ["Rural", "Urbana"])

# Filtro de raça
categorias_raca = df_categ_raca["categoria"].unique().tolist()
categoria_opcao = st.sidebar.selectbox("Raça:", categorias_raca)

# Filtro de Região
categorias_regiao = df_categ_regiao["categoria"].unique().tolist()
regiao_opcao = st.sidebar.multiselect("Região:", categorias_regiao)

# Filtro por Estados
categorias_estados = df_categ_estados["categoria"].unique().tolist()
estados_opcao = st.sidebar.multiselect("Estados:", categorias_estados)

###---------------------------FIM FILTROS -----------------------------

###---------------------------Gráficos -----------------------------

# Cria duas colunas para os gráficos
col1, col2 = st.columns(2)

# ----- GRÁFICO GERAL -----
with col1:
    titulo_geral = f"<h5 style='margin-bottom: 5px;'>Brasil - Sexo: {sexo_opcao} | Região: {reg_cadunico_opcao}</h5>"
    st.markdown(titulo_geral, unsafe_allow_html=True)
    df_filtrado = df_categ_geral.query("sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao")
    plot_zscore_brasil(df_filtrado)

# ----- GRÁFICO POR RAÇA -----
with col2:
    titulo_raca = f"<h5 style='margin-bottom: 5px;'>Raça: {categoria_opcao} | Sexo: {sexo_opcao} | Região: {reg_cadunico_opcao}</h5>"
    st.markdown(titulo_raca, unsafe_allow_html=True)
    df_raca = df_categ_raca.query("sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao "\
                                    "and categoria == @categoria_opcao")
    plot_zscore_brasil(df_raca)

# ----- GRÁFICO POR REGIÃO DO PAÍS -----
if regiao_opcao:
    titulo_geral = f"<h5 style='margin-bottom: 5px;'>Z-Score Idade x Região País x Cadastral - Sexo: {sexo_opcao} | Região Cadastral: {reg_cadunico_opcao} | Região: {regiao_opcao}</h5>"    
    df_regiao = df_categ_regiao.query("sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao "\
                                      "and categoria in(@regiao_opcao)")
else:
    titulo_geral = f"<h5 style='margin-bottom: 5px;'>Z-Score Idade x Região País x Cadastral - Sexo: {sexo_opcao} | Região Cadastral: {reg_cadunico_opcao} | Região: Todas</h5>"    
    df_regiao = df_categ_regiao.query("sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao ")

st.markdown(titulo_geral, unsafe_allow_html=True)

# Cria duas colunas para os gráficos
col1, col2, col3 = st.columns(3)

with col1:        
    titulo_geral = f"<h6 style='margin: 2px; text-align: center;'>Peso</h6>"
    st.markdown(titulo_geral, unsafe_allow_html=True)
    plot_zscore_por_regiao(df_regiao, 'med_peso')
with col2:    
    titulo_geral = f"<h6 style='margin: 2px; text-align: center;'>Altura</h6>"
    st.markdown(titulo_geral, unsafe_allow_html=True)
    plot_zscore_por_regiao(df_regiao, 'med_altura')
with col3:    
    titulo_geral = f"<h6 style='margin: 2px; text-align: center;'>IMC</h6>"
    st.markdown(titulo_geral, unsafe_allow_html=True)
    plot_zscore_por_regiao(df_regiao, 'med_imc')


# ----- GRÁFICO POR ESTADOS -----

# Filtro por região dos estados
if regiao_opcao:
    df_estados = df_categ_estados.query("sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao and regiao in @regiao_opcao")
else:
    df_estados = df_categ_estados.query("sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao")

# Depois aplica o filtro de estados, se houver
if estados_opcao:
    df_estados = df_estados[df_estados["categoria"].isin(estados_opcao)]


if estados_opcao:
    #titulo_geral = f"<h5 style='margin-bottom: 5px;'>Z-Score Idade x Estado - Sexo: {sexo_opcao} | Estado: {estados_opcao}</h5>"    
    # df_estados = df_categ_estados.query("sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao "\
    #                                   " and categoria in(@estados_opcao)")    
    df_estados = df_estados[df_estados["categoria"].isin(estados_opcao)]

else:   
    titulo_geral = f"<h5 style='margin-bottom: 5px;'>Z-Score Idade x Estado - Sexo: {sexo_opcao} | Estado: Todos</h5>"    
    #df_estados = df_categ_estados.query("sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao ")

estados_str = ", ".join(estados_opcao) if estados_opcao else "Todos"
regioes_str = ", ".join(regiao_opcao) if regiao_opcao else "Todas"

titulo_geral = f"<h5 style='margin-bottom: 5px;'>Z-Score Idade x Estado - Sexo: {sexo_opcao} | Região Cadastral: {reg_cadunico_opcao} | Região: {regioes_str} | Estado: {estados_str}</h5>"
st.markdown(titulo_geral, unsafe_allow_html=True)

# Cria duas colunas para os gráficos
col1, col2, col3 = st.columns(3)

with col1:        
    titulo_geral = f"<h6 style='margin: 2px; text-align: center;'>Peso</h6>"
    st.markdown(titulo_geral, unsafe_allow_html=True)
    plot_zscore_por_estado(df_estados, 'med_peso')
with col2:    
    titulo_geral = f"<h6 style='margin: 2px; text-align: center;'>Altura</h6>"
    st.markdown(titulo_geral, unsafe_allow_html=True)
    plot_zscore_por_estado(df_estados, 'med_altura')
with col3:    
    titulo_geral = f"<h6 style='margin: 2px; text-align: center;'>IMC</h6>"
    st.markdown(titulo_geral, unsafe_allow_html=True)
    plot_zscore_por_estado(df_estados, 'med_imc')