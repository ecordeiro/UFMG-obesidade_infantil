import streamlit as st

st.set_page_config(page_title="Painel Principal", layout="wide")

st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3, h4, h5 {
        color: #2c3e50;
    }
    .english-text {
        color: #5a6c7d;
        font-style: italic;
        margin-top: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <h4 style='text-align: center; color: var(--text-color);'>
        📊 Indicadores Antropométricos de Crescimento Infantil em crianças de 0 a 9 anos 
        provenientes de famílias candidatas ou receptoras do Programa Bolsa Família do governo federal.
    </h4>
    """,
    unsafe_allow_html=True
)

st.markdown("""
Bem-vindo ao painel de indicadores antropométricos. Use o menu lateral para acessar as diferentes visualizações:

- 📊 Dados gerais
- 🌍 Dados por região
- 🎯 Dados por raça/cor
- 🏙️ Dados por estado
- 📌 Prevalência por raça/cor, estado, região e sexo
- 🇧🇷 Prevalência Brasil            
""")

# Nota técnica
st.markdown("---")
st.header("📋 Nota Técnica")

st.subheader("Sobre os Dados e a Plataforma (About the Data and the Platform)")
st.markdown("""
Esta plataforma apresenta os resultados do estudo **"Crescimento, Sobrepeso e Obesidade em Crianças Brasileiras: Coorte de Seis Milhões"**, 
que analisa a adequação dos principais índices antropométricos e a prevalência de sobrepeso e obesidade em crianças de 0 a 9 anos.
""")
st.markdown("""
<div class="english-text">
This platform presents results from the study "Growth, Overweight, and Obesity in Brazilian Children: A Cohort of Six Million", 
which analyzes the adequacy of key anthropometric indicators and the prevalence of overweight and obesity in children aged 0 to 9 years.
</div>
""", unsafe_allow_html=True)

st.subheader("Fontes de Dados (Data Sources)")
st.markdown("""
Os dados foram obtidos pela integração de três sistemas nacionais:

- **Cadastro Único (CadÚnico)** – informações socioeconômicas de famílias de baixa renda
- **Sistema de Informações sobre Nascidos Vivos (SINASC)** – dados de peso ao nascer e características do parto
- **Sistema de Vigilância Alimentar e Nutricional (SISVAN)** – medidas de peso e altura registradas na Atenção Primária à Saúde
""")
st.markdown("""
<div class="english-text">
Data were obtained through the integration of three national information systems:
<br><br>
- <b>Unified Registry (CadÚnico)</b> – socioeconomic data on low-income families<br>
- <b>Live Birth Information System (SINASC)</b> – data on birth weight and delivery characteristics<br>
- <b>Food and Nutrition Surveillance System (SISVAN)</b> – weight and height measures recorded in Primary Health Care
</div>
""", unsafe_allow_html=True)

st.subheader("Indicadores Calculados (Calculated Indicators)")
st.markdown("""
Com base nesses sistemas, foram calculados os seguintes indicadores em escores Z, seguindo a referência da OMS:

- **Peso para idade (WAZ)** / *Weight-for-age*
- **Altura para idade (HAZ)** / *Height-for-age*
- **Índice de Massa Corporal para idade (BMIZ)** / *Body Mass Index-for-age*

Esses indicadores permitem avaliar a adequação do crescimento e estimar a prevalência de sobrepeso e obesidade 
segundo sexo, idade, raça/cor e estado de nascimento.
""")
st.markdown("""
<div class="english-text">
Based on these systems, the following indicators were calculated according to WHO references:
<br><br>
- <b>Weight-for-age (WAZ)</b><br>
- <b>Height-for-age (HAZ)</b><br>
- <b>Body Mass Index-for-age (BMIZ)</b>
<br><br>
These indicators allow assessment of growth adequacy and estimation of overweight and obesity prevalence by sex, age, race/skin color, and state of birth.
</div>
""", unsafe_allow_html=True)

st.markdown("""
O sobrepeso e a obesidade em crianças menores de cinco anos foram definidos usando o z escore de IMC para a idade acima de dois e três 
desvios-padrão, respectivamente; para crianças de cinco a nove anos, foram definidos a um e dois desvios-padrão de escore z de IMC, 
respectivamente.
""")

st.markdown("""
<div class="english-text">
Overweight and obesity for children under five years of age were defined as BMI for age z-score above two and three standard deviations, children aged five to nine years were one and two standard deviations.
</div>
""", unsafe_allow_html=True)

st.subheader("Principais Achados (Key Findings)")
st.markdown("""
A análise evidencia importantes **desigualdades regionais e étnico-raciais**: enquanto parte das regiões brasileiras 
apresenta ganhos consistentes de altura, crianças indígenas e do Norte permanecem abaixo do padrão internacional. 
Ao mesmo tempo, observa-se aumento expressivo do sobrepeso e da obesidade nas regiões Sul e Sudeste.
""")
st.markdown("""
<div class="english-text">
The analysis reveals significant regional and ethno-racial inequalities: while some regions show consistent gains in height, 
Indigenous and Northern children remain below international standards. At the same time, there is a marked increase in 
overweight and obesity in the South and Southeast regions.
</div>
""", unsafe_allow_html=True)

st.subheader("Objetivo (Objective)")
st.markdown("""
O objetivo do painel é oferecer uma ferramenta interativa de visualização e análise que apoie pesquisadores, gestores e profissionais de saúde na formulação de políticas e estratégias voltadas à promoção do crescimento saudável e da alimentação adequada na infância.
""")
st.markdown("""
<div class="english-text">
The goal of this dashboard is to provide an interactive visualization and analysis tool to support researchers, 
policymakers, and health professionals in designing strategies and policies that promote healthy growth and adequate childhood nutrition.
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.subheader("🙏 Agradecimentos (Acknowledgments)")
st.markdown("""
**Instituições / Institutions:**
- Universidade Federal de Minas Gerais, Escola de Enfermagem (EEUFMG)
- Centro de Integração de Dados e Conhecimento em Saúde (CIDACS)
- Centro Federal de Educação Tecnológica de Minas Gerais (CEFET-MG)

**Financiamento / Funding:**

Esta plataforma recebeu financiamento da **Fundação de Pesquisa do Estado de Minas Gerais (FAPEMIG)**, APQ-01777-23, 
do Decit/SETICS/Ministério da Saúde e **Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq)**, 
número da bolsa 25000.148278/2022–10. 

O estudo também utilizou recursos do **Centro de Integração de Dados e Conhecimento em Saúde (CIDACS)**, 
que recebe financiamento da **Fundação Bill & Melinda Gates**, do **Wellcome Trust**, da Secretaria de Vigilância 
em Saúde do Ministério da Saúde e da Secretaria de Ciência e Tecnologia do Estado da Bahia (SECTI-BA).
""")
st.markdown("""
<div class="english-text">
This platform received funding from the <b>Research Foundation of the State of Minas Gerais (FAPEMIG)</b>, APQ-01777-23, 
from Decit/SETICS/Ministry of Health and the <b>National Council for Scientific and Technological Development (CNPq)</b>, 
grant number 25000.148278/2022–10.

The study also used resources from the <b>Center for Data and Knowledge Integration in Health (CIDACS)</b>, 
which receives funding from the <b>Bill & Melinda Gates Foundation</b>, the <b>Wellcome Trust</b>, the Health Surveillance 
Secretariat of the Ministry of Health, and the Science and Technology Secretariat of the State of Bahia (SECTI-BA).
</div>
""", unsafe_allow_html=True)

st.markdown("### Instituições Parceiras")

# Cria mais colunas para adicionar espaçamento nas laterais
col_space1, col1, col2, col3, col4, col5, col_space2 = st.columns([1, 2, 2, 2, 2, 2, 1])

with col1:
    st.image("images/cidacs.jpg", width=100)

with col2:
    st.image("images/ufmg.jpg", width=100)

with col3:
    st.image("images/ufcg.jpg", width=100)

with col4:
    st.image("images/UFRB.jpg", width=100)

with col5:
    st.image("images/UFBA.jpg", width=100)

st.markdown("---")