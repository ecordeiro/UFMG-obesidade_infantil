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
        name='Altura/Idade',
        marker=dict(symbol='circle', color='red', size=8),
        line=dict(color='red')
    ))

    fig.add_trace(go.Scatter(
        x=df['Idade'], y=df['med_imc'],
        mode='lines+markers',
        name='IMC/Idade',
        marker=dict(symbol='circle', color='deepskyblue', size=8),
        line=dict(color='deepskyblue')
    ))

    fig.add_trace(go.Scatter(
        x=df['Idade'], y=df['med_peso'],
        mode='lines+markers',
        name='Peso/Idade',
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
        title=dict(
            text="<b>escore Z Médio/Idade</b>",
            font=dict(color='black', size=16)
        ),
        # Força a cor preta para qualquer texto que não tenha cor específica
        font=dict(color='black'),
        
        # Ajuste do Eixo X
        xaxis=dict(
            title=dict(
                text="<b>Idade</b>",
                font=dict(color='black', size=14) # Cor preta explícita no label
            ),
            tickfont=dict(color='black', family='Arial Black', size=12), # Cor preta nos nomes das idades
            tickangle=45,
            showgrid=True,
            gridcolor='rgba(255,255,255,0.2)'
        ),
        
        # Ajuste do Eixo Y
        yaxis=dict(
            title=dict(
                text="<b>escore Z Médio</b>",
                font=dict(color='black', size=14) # Cor preta explícita no label
            ),
            tickfont=dict(color='black', family='Arial Black', size=12), # Cor preta nos números (-0.5, 0, 0.5)
            showgrid=True,
            gridcolor='rgba(255,255,255,0.2)'
        ),
        
        legend=dict(
            font=dict(color='black'),
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

    nomes_formatados = {
        "Brasil": "Brasil",
        "centro_oeste": "Centro Oeste",
        "nordeste": "Nordeste",
        "norte": "Norte",
        "sudeste": "Sudeste",
        "sul": "Sul"
    }

    fig = go.Figure()

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

    # Linha Z-Score = 0 (mantida em branco para contraste com as linhas coloridas)
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

    if medida == 'med_peso':
        label_y = 'Peso'
    elif medida == 'med_imc':
        label_y = 'IMC'
    else:
        label_y = 'Altura'

    fig.update_layout(
        height=350, # Aumentei um pouco para acomodar a legenda
        # 1. Título principal
        title=dict(
            text=f"<b>escore Z Médio de {label_y}/Idade por Região</b>",
            font=dict(color='black', size=16)
        ),
        # 2. Eixo X
        xaxis=dict(
            title=dict(text="<b>Idade</b>", font=dict(color='black')),
            tickfont=dict(color='black', family='Arial Black', size=11),
            tickangle=45,
            showgrid=True,
            gridcolor='rgba(255,255,255,0.2)'
        ),
        # 3. Eixo Y
        yaxis=dict(
            title=dict(text=f"<b>escore Z Médio de {label_y}</b>", font=dict(color='black')),
            tickfont=dict(color='black', family='Arial Black', size=11),
            showgrid=True,
            gridcolor='rgba(255,255,255,0.2)'
        ),
        # 4. Legenda e Fonte Geral
        font=dict(color='black'),
        legend=dict(
            font=dict(color='black', size=10),
            orientation="v",
            yanchor="top",
            y=0.98,
            xanchor="right",
            x=0.98,
            bgcolor='rgba(255,255,255,0.3)' # Fundo leve na legenda para leitura
        ),
        margin=dict(t=60, b=40, l=50, r=20)
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_zscore_por_estado(df, medida='med_peso'):
    """
    Plota gráfico interativo de Z-Score médio por idade, por estado.
    Mantém a legenda original mas destaca os eixos e títulos.
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
            # Voltando para os tamanhos originais
            mode='lines+markers',
            name=estado,
            marker=dict(symbol='circle', size=8)
        ))

    # Linha Z-Score = 0
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

    if medida == 'med_peso':
        label_y = 'Peso'
    elif medida == 'med_imc':
        label_y = 'IMC'
    else:
        label_y = 'Altura'

    fig.update_layout(
        height=400,        
        # Título em preto e negrito
        title=dict(
            text=f"<b>escore Z Médio de {label_y}/Idade por Estado</b>",
            font=dict(color='black', size=16)
        ),
        # Eixo X: Label e Números em preto/negrito
        xaxis=dict(
            title=dict(text="<b>Idade</b>", font=dict(color='black')),
            tickfont=dict(color='black', family='Arial Black', size=11),
            tickangle=45,
            showgrid=True,
            gridcolor='rgba(255,255,255,0.2)'
        ),
        # Eixo Y: Label e Números em preto/negrito
        yaxis=dict(
            title=dict(text=f"<b>escore Z Médio de {label_y}</b>", font=dict(color='black')),
            tickfont=dict(color='black', family='Arial Black', size=11),
            showgrid=True,
            gridcolor='rgba(255,255,255,0.2)'
        ),
        # Fonte global preta
        font=dict(color='black'),
        # Restaurando a legenda para o padrão original (vê-se à direita)
        showlegend=True
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

    labels = ['Obesidade', 'Excesso de Peso', 'Sem Sobrepeso']
    values = [obesidade, excesso, saudavel]
    colors = ['#e74c3c', '#3498db', '#2ecc71']  # Vermelho, Azul, Verde

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        textinfo='percent+label',
        # Texto dentro das fatias em negrito para destacar no fundo colorido
        insidetextfont=dict(color='white', size=14, family='Arial Black'),
        hoverinfo='label+percent',
        sort=False
    )])

    fig.update_layout(
        # 1. Título em preto e negrito
        title=dict(
            text='<b>Dados Gerais de Obesidade e Excesso de Peso</b>',
            font=dict(color='black', size=16)
        ),
        # 2. Cor global preta (afeta hover e textos secundários)
        font=dict(color='black'),
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

    # Títulos dinâmicos com a tag de negrito
    titulo_texto = {
        'estado': '<b>Obesidade e Excesso de Peso por Estado e Região</b>',
        'regiao': '<b>Obesidade e Excesso de Peso por Região</b>',
        'raca': '<b>Obesidade e Excesso de Peso por Raça</b>'
    }[modo]

    fig.update_layout(
        height=450, # Aumentado levemente para não cortar os nomes externos
        # 1. Título em preto e negrito
        title=dict(
            text=titulo_texto,
            font=dict(color='black', size=16)
        ),
        # 2. Cor global preta
        font=dict(color='black'),
        template='plotly_white',
        polar=dict(
            # Cores das linhas radiais (as "teias")
            radialaxis=dict(
                showticklabels=True,
                ticks='',
                # Números da escala (ex: 10%, 20%) em preto
                tickfont=dict(color='black', family='Arial Black', size=10),
                angle=0,
                gridcolor='rgba(0,0,0,0.1)'
            ),
            # Rótulos externos (Nomes dos Estados/Regiões ao redor do gráfico)
            angularaxis=dict(
                tickmode='array',
                tickvals=df['Angulo'],
                ticktext=df['categoria'],
                # Força os nomes ao redor do círculo em preto e negrito
                tickfont=dict(color='black', family='Arial Black', size=11)
            )
        ),
        # 3. Legenda em preto
        legend=dict(
            font=dict(color='black', size=11),
            orientation='v', 
            yanchor='top'
        )
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_grafico_geral(df, colunas, titulo="Dados Gerais - IMC/Idade, peso/Idade e altura/Idade"):
    import plotly.graph_objects as go

    nome_legivel = {
        "med_altura": "Altura/Idade",
        "med_peso": "Peso/Idade",
        "med_imc": "IMC/Idade"
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
        # Adicionei <b> no texto dentro das barras para também ficar em negrito
        text=[f"<b>{v:.2f}</b>" for v in valores],
        textposition='inside',
        width=0.3,
        textfont=dict(color='black') # Garante cor preta no texto interno
    ))

    fig.update_layout(
        # 1. Título em preto e negrito
        title=dict(
            text=f"<b>{titulo}</b>",
            font=dict(color='black', size=14)
        ),
        yaxis=dict(
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='gray',
            showgrid=False,
            showticklabels=False
        ),
        # 2. Eixo X com labels pretos e em negrito
        xaxis=dict(
            showgrid=False,
            showticklabels=True,
            tickfont=dict(color='black', family='Arial Black', size=11)
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        # 3. Cor global da fonte como fallback
        font=dict(color='black', size=12),
        height=300,
        width=400,
        margin=dict(t=50, b=40, l=20, r=20),
        uniformtext_minsize=10,
        uniformtext_mode='hide'
    )

    return fig

def plot_grafico_geral_por_regiao(df_geral_regiao):
    """
    Exibe um gráfico de barras agrupadas com IMC, altura e peso médios por região no Streamlit.
    """

    # Cores fixas para cada variável
    cor_mapeada = {
        "med_altura": "#FF0000",  # vermelho
        "med_imc": "#00BFFF",     # azul claro
        "med_peso": "#00FF00"     # verde
    }

    # Criar figura
    fig = go.Figure()

    # Tratamento das categorias
    df_geral_regiao['categoria'] = (
        df_geral_regiao['categoria']
        .str.replace('_', ' ', regex=False)
        .str.title()
    )

    # Adicionar barras
    fig.add_trace(go.Bar(
        x=df_geral_regiao['categoria'],
        y=df_geral_regiao['med_altura'],
        name='Altura/Idade',
        marker_color=cor_mapeada['med_altura']
    ))
    fig.add_trace(go.Bar(
        x=df_geral_regiao['categoria'],
        y=df_geral_regiao['med_imc'],
        name='IMC/Idade',
        marker_color=cor_mapeada['med_imc']
    ))
    fig.add_trace(go.Bar(
        x=df_geral_regiao['categoria'],
        y=df_geral_regiao['med_peso'],
        name='Peso/Idade',
        marker_color=cor_mapeada['med_peso']
    ))

    # Layout do gráfico com ajustes de cor e negrito
    fig.update_layout(
        height=300,
        barmode='group',
        # 1. Título em preto e negrito
        title=dict(
            text='<b>escore Z médios por região</b>',
            font=dict(color='black', size=16)
        ),
        # 2. Eixo X (Nomes das Regiões)
        xaxis=dict(
            tickfont=dict(color='black', family='Arial Black', size=12),
            showgrid=False
        ),
        # 3. Eixo Y (Valores da escala)
        yaxis=dict(
            tickfont=dict(color='black', family='Arial Black', size=12),
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)' # Grid bem suave para não poluir
        ),
        # 4. Legenda e Fonte Geral
        font=dict(color='black'),
        legend=dict(
            font=dict(color='black', size=10),
            orientation="h", # Legenda horizontal costuma ficar melhor em gráficos de região
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(t=80, b=40, l=40, r=20) # Espaço extra para o título e legenda
    )

    # Mostrar no Streamlit
    st.plotly_chart(fig, use_container_width=True)