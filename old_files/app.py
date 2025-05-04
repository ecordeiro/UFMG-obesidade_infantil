# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Gráficos de Saúde Infantil", layout="centered")

st.title("Gráficos de Indicadores de Saúde Infantil")

# --- GRÁFICO 1: Z Score médio de peso para idade com setas em todos os pontos ---

st.subheader("Z Score médio de peso para idade (com setas em cada intervalo de idade)")

# Dados simulados
data_zscore = {
    "Idade": ["0 - 5m", "06 - 11m", "12 - 17m", "18 - 23m", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a"],
    "Grupo A": [0.1, 0.3, 0.2, 0.2, 0.1, 0.0, 0.05, 0.1, 0.15, 0.2, 0.22, 0.25],
    "Grupo B": [0.0, 0.2, 0.2, 0.1, 0.0, -0.1, -0.05, 0.0, 0.05, 0.1, 0.1, 0.15],
    "Grupo C": [-0.1, 0.0, 0.05, 0.0, -0.2, -0.4, -0.5, -0.45, -0.35, -0.25, -0.2, -0.2],
    "Grupo D": [0.2, 0.3, 0.35, 0.3, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.52, 0.55]
}
df_z = pd.DataFrame(data_zscore)
idades = df_z["Idade"]

grupos = ["Grupo A", "Grupo B", "Grupo C", "Grupo D"]
cores1 = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

fig1 = go.Figure()

for i, grupo in enumerate(grupos):
    y_vals = df_z[grupo]
    
    # Linha base
    fig1.add_trace(go.Scatter(
        x=idades,
        y=y_vals,
        mode="lines",
        name=grupo,
        line=dict(color=cores1[i])
    ))

    # Adiciona uma seta entre cada par consecutivo de pontos
    for j in range(len(idades) - 1):
        x0 = idades[j]
        x1 = idades[j+1]
        y0 = y_vals.iloc[j]
        y1 = y_vals.iloc[j+1]

        fig1.add_annotation(
            x=x1, y=y1,
            ax=x0, ay=y0,
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=3,
            arrowsize=1,
            arrowwidth=1.5,
            arrowcolor=cores1[i],
            opacity=0.9
        )

fig1.update_layout(
    title="Z Score médio de peso para idade",
    xaxis_title="Idade",
    yaxis_title="Z Score",
    title_x=0.5,
    shapes=[
        dict(
            type="line",
            xref="paper",  # Usa toda a largura do gráfico
            x0=0, x1=1,
            y0=0, y1=0,
            line=dict(
                color="purple",
                width=2,
                dash="solid"  # Pode trocar por "dot", "solid" etc.
            )
        )
    ]
)


st.plotly_chart(fig1)


# --- GRÁFICO 2: IMC por Altura com SETAS ---

st.subheader("IMC por Altura e Raça/Cor (com setas)")

# Dados simulados para gráfico 2
data_imc = {
    "Altura (cm)": [110, 120, 130, 110, 120, 130, 110, 120, 130, 110, 120, 130, 110, 120, 130, 110, 120, 130],
    "IMC (kg/m²)": [15.5, 16.5, 17.5, 15.3, 16.3, 17.3, 15.8, 16.8, 17.8,
                    15.6, 16.6, 17.6, 15.7, 16.7, 17.7, 15.9, 16.9, 18.0],
    "Raça/Cor": ["Branca"]*3 + ["Preta"]*3 + ["Amarela"]*3 + ["Parda"]*3 + ["Indígena"]*3 + ["Outra"]*3
}
df_imc = pd.DataFrame(data_imc)

# Grupos e cores
racas = df_imc["Raça/Cor"].unique()
cores2 = ["#1f77b4", "#2ca02c", "#ff7f0e", "#d62728", "#9467bd", "#8c564b"]

fig2 = go.Figure()

for i, raca in enumerate(racas):
    df_grupo = df_imc[df_imc["Raça/Cor"] == raca].sort_values("Altura (cm)")
    
    # Linha principal
    fig2.add_trace(go.Scatter(
        x=df_grupo["Altura (cm)"],
        y=df_grupo["IMC (kg/m²)"],
        mode="lines",
        name=raca,
        line=dict(color=cores2[i])
    ))
    
    # Setas no final
    x0 = df_grupo["Altura (cm)"].iloc[-2]
    y0 = df_grupo["IMC (kg/m²)"].iloc[-2]
    x1 = df_grupo["Altura (cm)"].iloc[-1]
    y1 = df_grupo["IMC (kg/m²)"].iloc[-1]
    
    fig2.add_annotation(
        x=x1, y=y1,
        ax=x0, ay=y0,
        xref="x", yref="y",
        axref="x", ayref="y",
        showarrow=True,
        arrowhead=3,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor=cores2[i],
        opacity=0.9
    )

fig2.update_layout(
    title="IMC por Altura e Raça/Cor",
    xaxis_title="Altura (cm)",
    yaxis_title="IMC (kg/m²)",
    title_x=0.5
)

st.plotly_chart(fig2)

#---------> grafico 3: Distribuição por Categoria e Regiões Mapeadas
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import colorsys

# Configuração da página
st.title("Crianças de 5 anos")

# Criar dados de exemplo (substitua pelos seus dados reais)
regioes = {
    'Centro-Oeste': ['Distrito Federal', 'Goiás', 'Mato Grosso', 'Mato Grosso do Sul'],
    'Nordeste': ['Alagoas', 'Bahia', 'Ceará', 'Maranhão', 'Paraíba', 'Pernambuco', 'Piauí', 'Rio Grande do Norte', 'Sergipe'],
    'Norte': ['Acre', 'Amapá', 'Amazonas', 'Pará', 'Rondônia', 'Roraima', 'Tocantins'],
    'Sudeste': ['Espírito Santo', 'Minas Gerais', 'Rio de Janeiro', 'São Paulo'],
    'Sul': ['Paraná', 'Rio Grande do Sul', 'Santa Catarina']
}

# Definir cores base por região
cores_base = {
    'Centro-Oeste': 'rgb(214, 39, 40)',  # vermelho
    'Nordeste': 'rgb(31, 119, 180)',     # azul
    'Norte': 'rgb(44, 160, 44)',         # verde
    'Sudeste': 'rgb(148, 103, 189)',     # roxo
    'Sul': 'rgb(255, 127, 14)'           # laranja
}

# Função para criar versões mais claras das cores
def criar_cor_clara(cor_rgb):
    # Extrair os valores RGB
    r, g, b = map(int, cor_rgb.replace('rgb(', '').replace(')', '').split(','))
    
    # Converter para HSL para ajustar a luminosidade
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    
    # Criar versão mais clara (aumentar luminosidade)
    r_claro, g_claro, b_claro = colorsys.hls_to_rgb(h, min(l * 1.5, 0.9), s)
    
    return f'rgb({int(r_claro*255)}, {int(g_claro*255)}, {int(b_claro*255)})'

# Criar cores claras para não-obesos
cores = {}
for regiao, cor in cores_base.items():
    cores[regiao] = {
        'Obeso': cor,  # Mantém a cor original para obesos
        'Não-Obeso': criar_cor_clara(cor)  # Versão mais clara para não-obesos
    }

# Criar DataFrame com dados de obesidade
data = []
for regiao, estados in regioes.items():
    for estado in estados:
        valor_total = np.random.randint(20, 41)
        # Dividir o valor entre obesos e não-obesos
        valor_obeso = np.random.randint(5, valor_total // 2)
        valor_nao_obeso = valor_total - valor_obeso
        
        data.append({'Estado': estado, 'Região': regiao, 'Categoria': 'Obeso', 'Valor': valor_obeso})
        data.append({'Estado': estado, 'Região': regiao, 'Categoria': 'Não-Obeso', 'Valor': valor_nao_obeso})

df = pd.DataFrame(data)

# Criar o gráfico polar
fig = go.Figure()

# Ordenar os dados para visualização
df_ordenado = df.sort_values(['Região', 'Estado', 'Categoria'], ascending=[True, True, False])

# Preparar os dados para o gráfico
estados_unicos = df_ordenado['Estado'].unique()
theta = []
r = []
colors = []
hover_texts = []

# Para cada estado, adicionar as categorias na ordem correta
for estado in estados_unicos:
    dados_estado = df_ordenado[df_ordenado['Estado'] == estado]
    
    for _, row in dados_estado.iterrows():
        theta.append(estado)
        r.append(row['Valor'])
        
        # Selecionar a cor baseada na região e categoria
        cor = cores[row['Região']][row['Categoria']]
        colors.append(cor)
        
        hover_texts.append(f"{estado} - {row['Categoria']}: {row['Valor']}%")

# Adicionar o trace principal
fig.add_trace(go.Barpolar(
    r=r,
    theta=theta,
    marker_color=colors,
    marker_line_color="white",
    marker_line_width=0.5,
    opacity=0.8,
    hoverinfo="text",
    hovertext=hover_texts,
    width=0.8  # Largura das barras
))

# Configurar layout
fig.update_layout(
    title="",
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 40],
            tickvals=[10, 20, 30, 40],
            ticktext=["10%", "20%", "30%", "40%"],
            tickangle=0,
            gridcolor='lightgray',
            linecolor='lightgray'
        ),
        angularaxis=dict(
            direction="clockwise",
            tickfont_size=10,
        )
    ),
    width=800,
    height=800,
    template="plotly_white",
)

# Layout em colunas
col1, col2 = st.columns([3, 1])

with col1:
    # Exibir o gráfico
    st.plotly_chart(fig)

with col2:
    # Exibir legenda para regiões
    st.markdown("### Região")
    for regiao, cor_dict in cores.items():
        st.markdown(
            f"<div style='display:flex; align-items:center; margin-bottom:5px;'>"
            f"<div style='width:20px; height:20px; background-color:{cor_dict['Obeso']}; margin-right:10px;'></div>"
            f"<div>{regiao}</div>"
            f"</div>",
            unsafe_allow_html=True
        )
    
    # Exibir legenda para categorias de obesidade
    st.markdown("### Categoria")
    # Usando a primeira região apenas para demonstrar as cores
    primeira_regiao = list(cores.keys())[0]
    st.markdown(
        f"<div style='display:flex; align-items:center; margin-bottom:5px;'>"
        f"<div style='width:20px; height:20px; background-color:{cores[primeira_regiao]['Obeso']}; margin-right:10px;'></div>"
        f"<div>Com obesidade</div>"
        f"</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='display:flex; align-items:center;'>"
        f"<div style='width:20px; height:20px; background-color:{cores[primeira_regiao]['Não-Obeso']}; margin-right:10px;'></div>"
        f"<div>Sem obesidade</div>"
        f"</div>",
        unsafe_allow_html=True
    )

    # Opções para interatividade (se necessário)
    st.markdown("### Opções")
    if st.checkbox("Mostrar dados brutos", False):
        st.write(df)