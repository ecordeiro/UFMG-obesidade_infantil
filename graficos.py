import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import plotly.express as px
import numpy as np

def plot_zscore_brasil(df):
    """
    Plota um gráfico interativo com Z-Scores médios por idade no Brasil.
    Requer colunas: 'idade_cat', 'med_altura', 'med_imc', 'med_peso'.
    """

    ordem_idades = [
        "0 - 5m", "06 - 11m", "12 - 17m", "18 - 23m", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a"
    ]
    df['Idade'] = pd.Categorical(df['idade_cat'], categories=ordem_idades, ordered=True)
    df = df.sort_values('Idade')

    fig = go.Figure()

    # Linhas com setas para frente
    fig.add_trace(go.Scatter(
        x=df['Idade'], y=df['med_altura'],
        mode='lines+markers',
        name='Altura para Idade',
        marker=dict(symbol='arrow-right', color='red', size=8),
        line=dict(color='red')
    ))

    fig.add_trace(go.Scatter(
        x=df['Idade'], y=df['med_imc'],
        mode='lines+markers',
        name='IMC para Idade',
        marker=dict(symbol='arrow-right', color='deepskyblue', size=8),
        line=dict(color='deepskyblue')
    ))

    fig.add_trace(go.Scatter(
        x=df['Idade'], y=df['med_peso'],
        mode='lines+markers',
        name='Peso para Idade',
        marker=dict(symbol='arrow-right', color='limegreen', size=8),
        line=dict(color='limegreen')
    ))

    # Linha horizontal Z = 0 destacada
    fig.add_shape(
        type="line",
        x0=-0.5, x1=len(df['Idade']) - 0.5,
        y0=0, y1=0,
        line=dict(color="white", width=3, dash="dot")
    )

    # Texto explicativo
    fig.add_annotation(
        x=ordem_idades[0], y=0,
        text="Z-Score = 0",
        showarrow=False,
        yshift=15,
        font=dict(color='white', size=12)
    )

    fig.update_layout(
        height=400,        
        title="Z-Score Médio por Idade",
        xaxis_title="Idade",
        yaxis_title="Z-Score Médio",        
        xaxis=dict(
            tickangle=45,
            showgrid=True,
            gridcolor='rgba(255,255,255,0.2)'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.2)'
        )        
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_zscore_por_regiao(df, medida='med_peso'):
    """
    Plota gráfico interativo de Z-Score médio por idade, por região.
    """

    ordem_idades = [
        "0 - 5m", "06 - 11m", "12 - 17m", "18 - 23m", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a"
    ]
    df['Idade'] = pd.Categorical(df['idade_cat'], categories=ordem_idades, ordered=True)
    df = df.sort_values('Idade')

    # Cores fixas por região
    cores = {
        "Brasil": "red",
        "centro_oeste": "deepskyblue",
        "nordeste": "limegreen",
        "norte": "silver",
        "sudeste": "orange",
        "sul": "yellow"
    }

    # Inicia figura
    fig = go.Figure()

    # Plota cada região
    for regiao in df['categoria'].unique():
        dados_regiao = df[df['categoria'] == regiao]
        fig.add_trace(go.Scatter(
            x=dados_regiao['Idade'],
            y=dados_regiao[medida],
            mode='lines+markers',
            name=regiao,
            marker=dict(symbol='arrow-right', size=8, color=cores.get(regiao, 'white')),
            line=dict(color=cores.get(regiao, 'white'))
        ))

    # Linha Z-Score = 0 destacada
    fig.add_shape(
        type="line",
        x0=-0.5, x1=len(ordem_idades)-0.5,
        y0=0, y1=0,
        line=dict(color="white", width=3, dash="dot")
    )

    fig.add_annotation(
        x=ordem_idades[0], y=0,
        text="Z-Score = 0",
        showarrow=False,
        yshift=15,
        font=dict(color='white', size=12)
    )

    # Label do eixo y adaptável
    if medida == 'med_peso':
        label_y = 'Peso'
    elif medida == 'med_imc':
        label_y = 'IMC'
    else:
        label_y = 'Altura'

    fig.update_layout(
        height=400,        
        title=f"Z-Score Médio de {label_y} para Idade por Região",
        xaxis_title="Idade",
        yaxis_title=f"Z-Score Médio de {label_y}",
        #plot_bgcolor='black',
        #paper_bgcolor='black',
        #font=dict(color='white'),
        xaxis=dict(
            tickangle=45,
            showgrid=True,
            gridcolor='rgba(255,255,255,0.2)'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.2)'
        ),        
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_zscore_por_estado(df, medida='med_peso'):
    """
    Plota gráfico interativo de Z-Score médio por idade, por estado.
    Requer colunas: 'idade_cat', 'categoria' (estado), e a medida escolhida.
    """

    ordem_idades = [
        "0 - 5m", "06 - 11m", "12 - 17m", "18 - 23m", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a"
    ]
    df['Idade'] = pd.Categorical(df['idade_cat'], categories=ordem_idades, ordered=True)
    df = df.sort_values('Idade')

    fig = go.Figure()

    for estado in df['categoria'].unique():
        dados_estado = df[df['categoria'] == estado]
        fig.add_trace(go.Scatter(
            x=dados_estado['Idade'],
            y=dados_estado[medida],
            mode='lines+markers',
            name=estado,
            marker=dict(symbol='arrow-right', size=8),
            line=dict()
        ))

    # Linha Z-Score = 0 destacada
    fig.add_shape(
        type="line",
        x0=-0.5, x1=len(ordem_idades)-0.5,
        y0=0, y1=0,
        line=dict(color="white", width=3, dash="dot")
    )

    fig.add_annotation(
        x=ordem_idades[0], y=0,
        text="Z-Score = 0",
        showarrow=False,
        yshift=15,
        font=dict(color='white', size=12)
    )

    # Label do eixo y
    if medida == 'med_peso':
        label_y = 'Peso'
    elif medida == 'med_imc':
        label_y = 'IMC'
    else:
        label_y = 'Altura'

    fig.update_layout(
        height=400,        
        title=f"Z-Score Médio de {label_y} para Idade por Estado",
        xaxis_title="Idade",
        yaxis_title=f"Z-Score Médio de {label_y}",
        #plot_bgcolor='black',
        #paper_bgcolor='black',
        #font=dict(color='white'),
        xaxis=dict(
            tickangle=45,
            showgrid=True,
            gridcolor='rgba(255,255,255,0.2)'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.2)'
        ),        
    )

    st.plotly_chart(fig, use_container_width=True)

def gerar_grafico_imc_altura(dados: pd.DataFrame, altura_col='Altura', imc_col='IMC', categoria_col='categoria'):
    """
    Gera um gráfico de linha de IMC vs Altura categorizado por Raça/Cor.
    
    Parâmetros:
    - dados: DataFrame contendo os dados
    - altura_col: nome da coluna de altura (em cm)
    - imc_col: nome da coluna de IMC
    - categoria_col: nome da coluna categórica (ex: Raça/Cor)
    """
    fig = px.line(
        dados.sort_values(by=altura_col),
        x=altura_col,
        y=imc_col,
        color=categoria_col,
        markers=True,
        labels={
            altura_col: "Altura (cm)",
            imc_col: "IMC (kg/m²)",
            categoria_col: "Raça/Cor"
        },
        title="IMC por Altura e Raça/Cor"
    )
    
    fig.update_layout(
        yaxis=dict(title="IMC (kg/m²)"),
        yaxis2=dict(overlaying='y', side='right', showgrid=False, title="IMC (kg/m²)"),        
    )
    
    st.plotly_chart(fig)

def gerar_grafico_radial_obesidade(df):
    # Cores por região
    cores_regiao = {
        'norte': '#1f77b4',
        'nordeste': '#ff7f0e',
        'sudeste': '#2ca02c',
        'sul': '#d62728',
        'centro_oeste': '#9467bd',
    }

    nomes_legenda = {
        'norte': 'Norte',
        'nordeste': 'Nordeste',
        'sudeste': 'Sudeste',
        'sul': 'Sul',
        'centro_oeste': 'Centro Oeste'
    }

    # Ordenar os dados
    df = df.sort_values(by=['regiao', 'categoria'])
    df['Angulo'] = np.linspace(0, 360, len(df), endpoint=False)

    fig = go.Figure()

    # Loop por região para adicionar traços individualmente
    for regiao, cor in cores_regiao.items():
        dados_regiao = df[df['regiao'] == regiao]

        # Obesidade (barra interna)
        fig.add_trace(go.Barpolar(
            r=dados_regiao['prev_obesidade'],
            theta=dados_regiao['Angulo'],
            #name=regiao.capitalize(),  # Nome da legenda
            name=nomes_legenda.get(regiao, regiao.capitalize()),
            marker_color=cor,
            marker_line_color="black",
            marker_line_width=0.5,
            opacity=1.0,
            hovertext=dados_regiao['categoria'] + ' - Obesidade',
            hoverinfo='text+r',
        ))

        # Excesso de peso (barra externa, mais clara)
        fig.add_trace(go.Barpolar(
            r=dados_regiao['prev_excesso'],
            theta=dados_regiao['Angulo'],
            name=None,  # Evita duplicar legenda
            marker_color=cor,
            marker_line_color="black",
            marker_line_width=0.4,
            opacity=0.5,
            hovertext=dados_regiao['categoria'] + ' - Excesso de peso',
            hoverinfo='text+r',
            showlegend=False  # Oculta da legenda
        ))

    fig.update_layout(        
        height=400,        
        title='Obesidade e Excesso de Peso por Estado e Região',
        template='plotly_white',
        polar=dict(
            radialaxis=dict(
                showticklabels=True,
                ticks='',
                tickfont=dict(color='black', size=10),  # Cor e tamanho dos valores
                angle=0,  # Define a orientação do eixo radial
                #gridcolor='gray',       # <- cor das linhas do radar
                #gridwidth=1,          # <- espessura da linha
                #linecolor='black',      # <- borda do eixo radial
                #linewidth=1
            ),
            angularaxis=dict(
                tickmode='array',
                tickvals=df['Angulo'],
                ticktext=df['categoria']                
            )
        ),
        legend=dict(orientation='v', yanchor='top')        
    )

    st.plotly_chart(fig, use_container_width=True)
