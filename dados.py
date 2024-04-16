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
#print(df_principal) - Renomenado as colunas espeficicas.

df_principal['Var_pct'] = df_principal['var_dia_pct'] / 100
#print(df_principal) - A coluna var_dia_pct será em porcentagem agora

df_principal['valor_inicial'] = df_principal['valor_final'] / (df_principal['Var_pct'] + 1)
#print(df_principal) - Criando uam nova coluna para obter o valor inicial da ação

df_principal = df_principal.merge(df_total_acoes, left_on='Ativo', right_on='Código', how='left')
#print(df_principal) - - Utilizando o comando merge para a junção de duas tabelas com campos iguais

df_principal = df_principal.drop(columns=['Código'])
#print(df_principal) - Removendo as colunas duplicadas

df_principal['Variacao_rs'] = (df_principal['valor_final'] - df_principal['valor_inicial']) * df_principal['Qtde. Teórica']
#print(df_principal) - Criando nova coluna

pd.options.display.float_format = '{:.2f}'.format
#print(df_principal) - Mudando para float todos os números

df_principal['Qtde. Teórica'] = df_principal['Qtde. Teórica'].astype(int)
#print(df_principal) - Transformando a coluna Qtde. Teórica para tipo inteiro

df_principal = df_principal.rename(columns={'Qtde. Teórica':'Qtd_terorica'}).copy()
#print(df_principal) - Renomeando coluna 

df_principal['Resultado'] = df_principal['Variacao_rs'].apply(lambda x: 'Subiu' if x > 0 else ('Desceu' if x < 0 else 'Estável'))
#print(df_principal) - Criando nova coluna

df_principal = df_principal.merge(df_ticker, left_on='Ativo', right_on='Ticker', how='left')
df_principal = df_principal.drop(columns=['Ticker'])
#print(df_principal) - Juntando as Frameworks e apagando a coluna que se repete