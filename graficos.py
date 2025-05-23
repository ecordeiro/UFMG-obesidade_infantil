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
        
    fig.add_trace(go.Scatter(
        x=df['Idade'], y=df['med_altura'],
        mode='lines+markers',
        name='Altura',
        marker=dict(symbol='circle', color='red', size=8),
        line=dict(color='red')
    ))

    fig.add_trace(go.Scatter(
        x=df['Idade'], y=df['med_imc'],
        mode='lines+markers',
        name='IMC',
        marker=dict(symbol='circle', color='deepskyblue', size=8),
        line=dict(color='deepskyblue')
    ))

    fig.add_trace(go.Scatter(
        x=df['Idade'], y=df['med_peso'],
        mode='lines+markers',
        name='Peso',
        marker=dict(symbol='circle', color='limegreen', size=8),
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
        ),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.98,
            xanchor="right",
            x=0.98
        )        
    )

    #st.plotly_chart(fig, use_container_width=True)
    return fig

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

    # Nome formatado das regiões
    nomes_formatados = {
        "Brasil": "Brasil",
        "centro_oeste": "Centro Oeste",
        "nordeste": "Nordeste",
        "norte": "Norte",
        "sudeste": "Sudeste",
        "sul": "Sul"
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
            name=nomes_formatados.get(regiao, regiao),
            marker=dict(symbol='circle', size=8, color=cores.get(regiao, 'white')),
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
        height=300,        
        title=f"Z-Score Médio de {label_y} para Idade por Região",
        xaxis_title="Idade",
        yaxis_title=f"Z-Score Médio de {label_y}",        
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
            marker=dict(symbol='circle', size=8),
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
        height=300,        
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

def gerar_comparacao_obesidade_excesso(df):
    # Corrigir valores
    for col in ['prev_obesidade', 'prev_excesso']:
        df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

    # Usar a média (ou único valor, se só tiver uma linha)
    obesidade = df['prev_obesidade'].mean()
    excesso = df['prev_excesso'].mean()

    # Criar DataFrame para gráfico
    dados = pd.DataFrame({
        'Indicador': ['Obesidade', 'Excesso de Peso'],
        'Prevalência': [obesidade, excesso]
    })

    # Gráfico de barras horizontal
    fig = px.bar(
        dados,
        x='Prevalência',
        y='Indicador',
        orientation='h',
        text='Prevalência',
        title='Comparação entre Obesidade e Excesso de Peso'
    )

    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        xaxis_title='Prevalência (%)',
        yaxis_title='',
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)

def gerar_pizza_composicao_peso(df):
    # Corrigir e converter valores
    for col in ['prev_obesidade', 'prev_excesso']:
        df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

    obesidade = df['prev_obesidade'].mean()
    excesso = df['prev_excesso'].mean()
    saudavel = max(0, 100 - (obesidade + excesso))

    labels = ['Obesidade', 'Excesso de Peso', 'Peso Saudável']
    values = [obesidade, excesso, saudavel]
    colors = ['#e74c3c', '#3498db', '#2ecc71']  # Vermelho, Azul, Verde

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),  # ❌ sem borda branca
        textinfo='percent+label',
        textfont_size=16,
        insidetextfont=dict(color='white', size=14),
        hoverinfo='label+percent',  # ✅ remove duplicidade
        sort=False
    )])

    fig.update_layout(
        title_text='Dados Gerais de Obesidade e Excesso de Peso',
        showlegend=False,
        height=300,
        margin=dict(t=60, b=20, l=20, r=20)
    )

    st.plotly_chart(fig, use_container_width=True)

def gerar_grafico_radial_obesidade(df, modo='estado'):
    """
    Gera gráfico radial de obesidade e excesso de peso.

    Parâmetros:
        df (DataFrame): Dados com colunas apropriadas.
        modo (str): 'estado' para dados por estado e região,
                    'regiao' para dados agregados por região,
                    'raca' para dados agrupados por raça/cor.
    """

    # Cores por região
    cores_regiao = {
        'norte': '#1f77b4',
        'nordeste': '#ff7f0e',
        'sudeste': '#2ca02c',
        'sul': '#d62728',
        'centro_oeste': '#9467bd',
    }

    nomes_legenda_regiao = {
        'norte': 'Norte',
        'nordeste': 'Nordeste',
        'sudeste': 'Sudeste',
        'sul': 'Sul',
        'centro_oeste': 'Centro Oeste'
    }

    # Cores por raça
    cores_raca = {
        'branca': '#1f77b4',
        'preta': '#ff7f0e',
        'parda': '#2ca02c',
        'amarela': '#d62728',
        'indígena': '#9467bd',
        'ni': '#8c564b',
    }

    nomes_legenda_raca = {
        'branca': 'Branca',
        'preta': 'Preta',
        'parda': 'Parda',
        'amarela': 'Amarela',
        'indígena': 'Indígena',
        'ni': 'Não Informada',
    }

    # Validação
    if modo not in ['estado', 'regiao', 'raca']:
        raise ValueError("O parâmetro 'modo' deve ser 'estado', 'regiao' ou 'raca'.")

    if modo == 'estado':
        df = df.sort_values(by=['regiao', 'categoria'])
        grupos = df['regiao'].unique()
        cores = cores_regiao
        nomes_legenda = nomes_legenda_regiao
    elif modo == 'regiao':
        df = df.sort_values(by='categoria')
        grupos = df['categoria'].unique()
        cores = cores_regiao
        nomes_legenda = nomes_legenda_regiao
    elif modo == 'raca':
        df = df.sort_values(by='categoria')
        grupos = df['categoria'].unique()
        cores = cores_raca
        nomes_legenda = nomes_legenda_raca

    # Ângulos para posicionamento
    df['Angulo'] = np.linspace(0, 360, len(df), endpoint=False)

    fig = go.Figure()

    for grupo in grupos:
        if modo == 'estado':
            dados = df[df['regiao'] == grupo]
            chave = grupo.lower()
            nome_legenda = nomes_legenda.get(chave, grupo.capitalize())
        else:
            dados = df[df['categoria'] == grupo]
            chave = grupo.lower()
            nome_legenda = nomes_legenda.get(chave, grupo)

        cor = cores.get(chave, '#888')

        # Obesidade
        fig.add_trace(go.Barpolar(
            r=dados['prev_obesidade'],
            theta=dados['Angulo'],
            name=nome_legenda,
            marker_color=cor,
            marker_line_color="black",
            marker_line_width=0.5,
            opacity=1.0,
            hovertext=dados['categoria'] + ' - Obesidade: ' + dados['prev_obesidade'].round(1).astype(str) + '%',
            hoverinfo='text',
        ))

        # Excesso de peso
        fig.add_trace(go.Barpolar(
            r=dados['prev_excesso'],
            theta=dados['Angulo'],
            name=None,
            marker_color=cor,
            marker_line_color="black",
            marker_line_width=0.4,
            opacity=0.5,
            hovertext=dados['categoria'] + ' - Excesso de peso: ' + dados['prev_excesso'].round(1).astype(str) + '%',
            hoverinfo='text',
            showlegend=False
        ))

    # Títulos dinâmicos
    titulo = {
        'estado': 'Obesidade e Excesso de Peso por Estado e Região',
        'regiao': 'Obesidade e Excesso de Peso por Região',
        'raca': 'Obesidade e Excesso de Peso por Raça'
    }[modo]

    fig.update_layout(
        height=400,
        title=titulo,
        template='plotly_white',
        polar=dict(
            radialaxis=dict(
                showticklabels=True,
                ticks='',
                tickfont=dict(color='black', size=10),
                angle=0,
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

def plot_grafico_geral(df, colunas, titulo="Dados Gerais - IMC, Peso e Altura"):
    import plotly.graph_objects as go

    nome_legivel = {
        "med_altura": "Altura",
        "med_peso": "Peso",
        "med_imc": "IMC"
    }

    cor_mapeada = {
        "med_altura": "#FF0000",
        "med_imc": "#00BFFF",
        "med_peso": "#00FF00"
    }

    valores = df[colunas].iloc[0]
    variaveis_legiveis = [nome_legivel.get(var, var) for var in colunas]
    cores = [cor_mapeada.get(var, "#CCCCCC") for var in colunas]

    fig = go.Figure(go.Bar(
        x=variaveis_legiveis,
        y=valores,
        marker_color=cores,
        text=[f"{v:.2f}" for v in valores],
        textposition='inside',  # dentro da barra evita corte
        width=0.3
    ))

    fig.update_layout(
        title=titulo,
        yaxis=dict(
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='white',
            showgrid=False,
            showticklabels=False
        ),
        xaxis=dict(
            showgrid=False,
            showticklabels=True
        ),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white', size=12),
        height=300,
        width=400,  # largura realmente menor
        margin=dict(t=40, b=60, l=20, r=20),
        uniformtext_minsize=10,
        uniformtext_mode='hide'
    )

    return fig

def plot_grafico_geral_por_regiao(df_geral_regiao):
    """
    Exibe um gráfico de barras agrupadas com IMC, altura e peso médios por região no Streamlit.

    Parâmetros:
    - df_geral_regiao (pd.DataFrame): deve conter as colunas:
        - 'categoria': nome da região (ex: 'norte', 'sul', etc.)
        - 'med_imc': valor médio de IMC
        - 'med_altura': valor médio de altura
        - 'med_peso': valor médio de peso
    """

    # Cores fixas para cada variável
    cor_mapeada = {
        "med_altura": "#FF0000",  # vermelho
        "med_imc": "#00BFFF",     # azul claro
        "med_peso": "#00FF00"     # verde
    }

    # Criar figura
    fig = go.Figure()

    # Adicionar barras com cores fixas por variável
    fig.add_trace(go.Bar(
        x=df_geral_regiao['categoria'],
        y=df_geral_regiao['med_imc'],
        name='IMC',
        marker_color=cor_mapeada['med_imc']
    ))
    fig.add_trace(go.Bar(
        x=df_geral_regiao['categoria'],
        y=df_geral_regiao['med_altura'],
        name='Altura',
        marker_color=cor_mapeada['med_altura']
    ))
    fig.add_trace(go.Bar(
        x=df_geral_regiao['categoria'],
        y=df_geral_regiao['med_peso'],
        name='Peso',
        marker_color=cor_mapeada['med_peso']
    ))

    # Layout do gráfico
    fig.update_layout(
        height=300,
        barmode='group',
        title='IMC, Altura e Peso Médios por Região',
        xaxis_title='',  # Remove label do eixo x
        yaxis_title='',  # Remove label do eixo y
        legend_title=''  # Remove título da legenda
    )

    # Mostrar no Streamlit
    st.plotly_chart(fig)
