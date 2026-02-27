# ========================== IMPORTS ========================== #
import streamlit as st
from dataset import (
    df_categ_geral_prev, df_categ_regiao_prev,
    df_categ_estados_prev, df_categ_raca_prev
)
from graficos import (
    gerar_pizza_composicao_peso, gerar_grafico_radial_obesidade
)

# ====================== CONFIGURAÇÃO PÁGINA ================== #
st.set_page_config(page_title="📌 Prevalência de Obesidade", layout="wide")

st.markdown("""
<style>
    /* SELECTBOX - VALOR SELECIONADO VISÍVEL */
    div[data-baseweb="select"] > div > div {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #d0d5dd !important;
    }
    
    /* Texto do valor selecionado FORÇADO preto */
    div[data-baseweb="select"] span[title] {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Dropdown aberto - opções pretas */
    div[role="listbox"] div {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Opção hover */
    div[role="option"]:hover {
        background-color: #f3f4f6 !important;
        color: #111827 !important;
    }
    
    /* TABS (mantém) */
    div.stTabs [data-baseweb="tab"] {
        background-color: #fafbfc !important;
        color: #262730 !important;
    }
</style>
""", unsafe_allow_html=True)





# ======================= MAPEAMENTOS BASE ===================== #
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
df_categ_estados_prev["regiao"] = df_categ_estados_prev["categoria"].map(estados_para_regiao)

mapa_idades = {
    "0 - 5m": "0-5 meses",
    "06 - 11m": "6-11 meses",
    "12 - 17m": "12-17 meses",
    "18 - 23m": "18-23 meses",
    "2a": "2 anos",
    "3a": "3 anos",
    "4a": "4 anos",
    "5a": "5 anos",
    "6a": "6 anos",
    "7a": "7 anos",
    "8a": "8 anos",
    "9a": "9 anos",
}

mapa_labels = {
    "centro_oeste": "Centro Oeste",
    "sudeste": "Sudeste",
    "nordeste": "Nordeste",
    "norte": "Norte",
    "sul": "Sul"
}

# ======================== SIDEBAR (GERAL) ===================== #
st.sidebar.subheader("🧭 Filtros Gerais")

sexo_opcao = st.sidebar.radio("Sexo:", ["Masculino", "Feminino"], key="sexo")
reg_cadunico_opcao = st.sidebar.radio("Região Cadastral:", ["Rural", "Urbana"], key="reg_cad")
opcoes_idade = df_categ_estados_prev["idade_cat"].unique().tolist()
idade_opcao = st.sidebar.selectbox(
    "Idade:",
    opcoes_idade,
    format_func=lambda v: mapa_idades.get(v, v),
    key="idade"
)

# =========================== ABAS ============================ #
abas = st.tabs(["📊 Composição Geral", "📍 Por Região", "🗺️ Por Estado", "🌎 Por Raça"])

# -------------------- Aba 0: Composição Geral ---------------- #
with abas[0]:
    df = df_categ_geral_prev.query(
        "idade_cat == @idade_opcao and sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
    )
    idade_label = mapa_idades.get(idade_opcao, idade_opcao)
    st.caption(f"Filtros: Idade {idade_label}, Sexo {sexo_opcao}, Região {reg_cadunico_opcao}")
    gerar_pizza_composicao_peso(df)

# ----------------------- Aba 1: Região ----------------------- #
with abas[1]:
    # Filtros específicos DA ABA (no corpo da aba, não na sidebar)
    with st.expander("🌎 Filtros por Região", expanded=True):
        labels_reg = [mapa_labels[val] for val in df_categ_regiao_prev["categoria"].unique()]
        labels_escolhidos = st.multiselect(
            "Região:", sorted(set(labels_reg)), key="regiao_tab_regiao"
        )
        regiao_opcao = [orig for orig, label in mapa_labels.items() if label in labels_escolhidos]

    df = df_categ_regiao_prev.query(
        "idade_cat == @idade_opcao and sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
    )

    if regiao_opcao:
        df = df[df["categoria"].isin(regiao_opcao)]
        regiao_desc = [mapa_labels.get(x, x) for x in regiao_opcao]
    else:
        regiao_desc = "Todas"

    idade_label = mapa_idades.get(idade_opcao, idade_opcao)
    st.caption(f"Filtros: Idade {idade_label}, Sexo {sexo_opcao}, Região {reg_cadunico_opcao} | {regiao_desc}")
    gerar_grafico_radial_obesidade(df, modo='regiao')

# ----------------------- Aba 2: Estado ----------------------- #
with abas[2]:
    # Filtros específicos DA ABA (no corpo da aba, não na sidebar)
    with st.expander("🗺️ Filtros por Estado/Região", expanded=True):
        labels_est_reg = [mapa_labels[val] for val in df_categ_estados_prev["regiao"].dropna().unique()]
        labels_escolhidos_est = st.multiselect(
            "Região:", sorted(set(labels_est_reg)), key="regiao_tab_estado"
        )
        regiao_opcao_est = [orig for orig, label in mapa_labels.items() if label in labels_escolhidos_est]

        estados_lista = df_categ_estados_prev["categoria"].unique()
        estados_opcao = st.multiselect(
            "Estados:", sorted(estados_lista), key="estados_tab_estado"
        )

    df = df_categ_estados_prev.query(
        "idade_cat == @idade_opcao and sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
    )

    if regiao_opcao_est:
        df = df[df["regiao"].isin(regiao_opcao_est)]
        regiao_desc = [mapa_labels.get(x, x) for x in regiao_opcao_est]
    else:
        regiao_desc = "Todas"

    if estados_opcao:
        df = df[df["categoria"].isin(estados_opcao)]
        estado_desc = estados_opcao
    else:
        estado_desc = "Todos"

    idade_label = mapa_idades.get(idade_opcao, idade_opcao)
    st.caption(
        f"Filtros: Idade {idade_label}, Sexo {sexo_opcao}, "
        f"Região {reg_cadunico_opcao} | {regiao_desc} | {estado_desc}"
    )
    gerar_grafico_radial_obesidade(df, modo='estado')

# ------------------------ Aba 3: Raça ------------------------ #
with abas[3]:
    df = df_categ_raca_prev.query(
        "idade_cat == @idade_opcao and sexo == @sexo_opcao and region_cadunico == @reg_cadunico_opcao"
    )
    idade_label = mapa_idades.get(idade_opcao, idade_opcao)
    st.caption(f"Filtros: Idade {idade_label}, Sexo {sexo_opcao}, Região {reg_cadunico_opcao}")
    gerar_grafico_radial_obesidade(df, modo='raca')
