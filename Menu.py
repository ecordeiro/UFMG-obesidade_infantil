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
    </style>
""", unsafe_allow_html=True)

st.markdown(
    "<h4 style='text-align: left; color: white;'>📊 Indicadores Antropométricos de Crescimento Infantil</h4>",
    unsafe_allow_html=True
)

st.markdown("""
Bem-vindo ao painel de indicadores antropométricos. Use o menu lateral para acessar as diferentes visualizações:

- 📊 Categoria Geral
- 🎯 Categoria por Raça
- 🌍 Categoria por Região
- 🏙️ Categoria por Estado
- 📌 Prevalência por Categoria
""")
