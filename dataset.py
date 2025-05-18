import pandas as pd 
from pathlib import Path
import pandas as pd

caminho = Path("dados") / "originais" / "dados_categorias_sexo_region_cadunico.csv"

# Carregar os dados de Categorias e Sexo, separando por tabela
df_categorias_sexo = pd.read_csv(caminho,sep=',', decimal='.')
df_categ_geral =  df_categorias_sexo.query("tabela == 'geral'")
df_categ_regiao =  df_categorias_sexo.query("tabela == 'regiao'")
df_categ_estados =  df_categorias_sexo.query("tabela == 'estados'")
df_categ_raca =  df_categorias_sexo.query("tabela == 'raca'")

caminho = Path("dados") / "originais" / "dados_categorias_sexo_region_cadunico_prev.csv"
df_categorias_prevalencia = pd.read_csv(caminho,sep=',', decimal='.')       

df_categ_geral_prev =  df_categorias_prevalencia.query("tabela == 'geral'")
df_categ_regiao_prev =  df_categorias_prevalencia.query("tabela == 'regiao'")
df_categ_estados_prev =  df_categorias_prevalencia.query("tabela == 'estados'")
df_categ_raca_prev =  df_categorias_prevalencia.query("tabela == 'raca'")


caminho = Path("dados") / "originais" / "dados_gerais_sexo_region_cadunico_prev.csv"
df_gerais_prevalencia = pd.read_csv(caminho,sep=',', decimal='.')       

df_geral_prev =  df_gerais_prevalencia.query("tabela == 'geral'")
df_geral_regiao_prev =  df_gerais_prevalencia.query("tabela == 'regiao'")
df_geral_estados_prev =  df_gerais_prevalencia.query("tabela == 'estados'")
df_geral_raca_prev =  df_gerais_prevalencia.query("tabela == 'raca'")


caminho = Path("dados") / "originais" / "dados_gerais_sexo_region_cadunico.csv"

# Carregar os dados de Categorias e Sexo, separando por tabela
df_gerais = pd.read_csv(caminho,sep=',', decimal='.')
df_geral_geral =  df_gerais.query("tabela == 'geral'")
df_geral_regiao =  df_gerais.query("tabela == 'regiao'")
df_geral_estados =  df_gerais.query("tabela == 'estados'")
df_geral_raca =  df_gerais.query("tabela == 'raca'")

