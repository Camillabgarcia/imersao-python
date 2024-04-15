import pandas as pd

df_principal = pd.read_excel('D:\\1USUARIOMASTER12-01-2024\\Desktop\\Alura-Python\\dados.xlsx.xlsx', sheet_name='Principal')
#print(df_principal.head(5)) - Mostra as 5 primeiras linhas da aba Principal

df_total_acoes = pd.read_excel('D:\\1USUARIOMASTER12-01-2024\\Desktop\\Alura-Python\\dados.xlsx.xlsx', sheet_name='Total_de_acoes')
#print(df_total_acoes) - Mostra a aba Total_de_acoes

df_ticker = pd.read_excel('D:\\1USUARIOMASTER12-01-2024\\Desktop\\Alura-Python\\dados.xlsx.xlsx', sheet_name='Ticker')
#print(df_ticker)

df_principal = df_principal[['Ativo', 'Data', 'Último (R$)', 'Var. Dia (%)']].copy()
#print(df_principal) - Seleciona colunas específicas

df_principal = df_principal.rename(columns={'Último (R$)':'valor_final', 'Var. Dia (%)':'var_dia_pct'}).copy()
#print(df_principal) - Renomeando as colunas
