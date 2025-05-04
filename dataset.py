import pandas as pd 

# Carregar os dados de Categorias e Sexo, separando por tabela
df_categorias_sexo = pd.read_csv(r'dados\originais\dados_categorias_sexo_region_cadunico.csv')
df_categ_geral =  df_categorias_sexo.query("tabela == 'geral'")
df_categ_regiao =  df_categorias_sexo.query("tabela == 'regiao'")
df_categ_estados =  df_categorias_sexo.query("tabela == 'estados'")
df_categ_raca =  df_categorias_sexo.query("tabela == 'raca'")


df_categorias_prevalencia = pd.read_csv(r'dados\originais\dados_categorias_sexo_region_cadunico_prev.csv')       

df_categ_geral_prev =  df_categorias_prevalencia.query("tabela == 'geral'")
df_categ_regiao_prev =  df_categorias_prevalencia.query("tabela == 'regiao'")
df_categ_estados_prev =  df_categorias_prevalencia.query("tabela == 'estados'")
df_categ_raca_prev =  df_categorias_prevalencia.query("tabela == 'raca'")
