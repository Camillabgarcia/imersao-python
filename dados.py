import pandas as pd
import plotly.express as px

df_principal = pd.read_excel('D:\\1USUARIOMASTER12-01-2024\\Desktop\\Alura-Python\\Planilha de Dados (1).xlsx', sheet_name='Principal')
#print(df_principal.head(5)) - Mostra as 5 primeira linhas

df_total_acoes = pd.read_excel('D:\\1USUARIOMASTER12-01-2024\\Desktop\\Alura-Python\\Planilha de Dados (1).xlsx', sheet_name='Total_de_acoes')
#print(df_total_acoes) - Mostra a aba Total_de_acoes

df_ticker = pd.read_excel('D:\\1USUARIOMASTER12-01-2024\\Desktop\\Alura-Python\\Planilha de Dados (1).xlsx', sheet_name='Ticker')
#print(df_ticker)

df_chatgpt = pd.read_excel('D:\\1USUARIOMASTER12-01-2024\\Desktop\\Alura-Python\\Planilha de Dados (1).xlsx', sheet_name='ChatGPT')
#print(df_chatgpt)

df_principal = df_principal[['Ativo', 'Data', 'Último (R$)', 'Var. Dia (%)']].copy()
#print(df_principal)  - Seleciona colunas específicas

df_principal = df_principal.rename(columns={'Último (R$)':'valor_final', 'Var. Dia (%)':'var_dia_pct'}).copy()
#print(df_principal) - - Renomenado as colunas espeficicas.

df_principal['Var_pct'] = df_principal['var_dia_pct'] / 100
#print(df_principal) - A coluna var_dia_pct será em porcentagem agora

df_principal['valor_inicial'] = df_principal['valor_final'] / (df_principal['Var_pct'] + 1)
#print(df_principal) - Criando uam nova coluna para obter o valor inicial da ação

df_principal = df_principal.merge(df_total_acoes, left_on='Ativo', right_on='Código', how='left')
#print(df_principal) - Utilizando o comando merge para a junção de duas tabelas com campos iguais

df_principal = df_principal.drop(columns=['Código'])
#print(df_principal) - Removendo as colunas duplicadas

df_principal['Variacao_rs'] = (df_principal['valor_final'] - df_principal['valor_inicial']) * df_principal['Qtde. Teórica']
#print(df_principal) - Criando nova coluna

pd.options.display.float_format = '{:.2f}'.format
#print(df_principal) - Mudando para float todos os números

df_principal['Qtde. Teórica'] = df_principal['Qtde. Teórica'].astype(int)
#print(df_principal) - Transformando a coluna Qtde. Teórica para tipo inteiro

df_principal = df_principal.rename(columns={'Qtde. Teórica':'Qtd_teorica'}).copy()
#print(df_principal) - Renomeando coluna

df_principal['Resultado'] = df_principal['Variacao_rs'].apply(lambda x: 'Subiu' if x > 0 else ('Desceu' if x < 0 else 'Estável'))
#print(df_principal) - Criando nova coluna

df_principal = df_principal.merge(df_ticker, left_on='Ativo', right_on='Ticker', how='left')
df_principal = df_principal.drop(columns=['Ticker'])
#print(df_principal) - Juntando as tabelas e apagando as colunas que estão repetidas

df_principal = df_principal.merge(df_chatgpt, left_on='Nome', right_on='Nome da Empresa', how='left')
df_principal = df_principal.drop(columns=['Nome da Empresa'])
#print(df_principal) - Juntando as tabelas e apagando as colunas que estão repetidas

df_principal['Cat_idade'] = df_principal['Idade (anos)'].apply(lambda x: 'Mais de 100 anos' if x > 100 else ('Menos de 50' if x < 50 else 'Entre 50 a 100'))
#print(df_principal) - Criando nova coluna

# Calculando os resultados
maior = df_principal['Variacao_rs'].max()
menor = df_principal['Variacao_rs'].min()
media = df_principal['Variacao_rs'].mean()
media_subiu = df_principal[df_principal['Resultado'] == 'Subiu']['Variacao_rs'].mean()
media_desceu = df_principal[df_principal['Resultado'] == 'Desceu']['Variacao_rs'].mean()

# Formatando os resultados
maior_formatado = f"R$ {maior:,.2f}"
menor_formatado = f"R$ {menor:,.2f}"
media_formatado = f"R$ {media:,.2f}"
media_subiu_formatado = f"R$ {media_subiu:,.2f}"
media_desceu_formatado = f"R$ {media_desceu:,.2f}"

#print("Maior:", maior_formatado)
#print("Menor:", menor_formatado)
#print("Média:", media_formatado)
#print("Média de quem subiu:", media_subiu_formatado)
#print("Média de quem desceu:", media_desceu_formatado)

df_principal_subiu = df_principal[df_principal['Resultado'] == 'Subiu']
#print(df_principal_subiu) - Criando um Dataframe apenas com as ações que subiram

df_analise_segmento = df_principal_subiu.groupby('Segmento')['Variacao_rs'].sum().reset_index()
#print(df_analise_segmento) - Soma agrupada por segmento

df_analise_saldo = df_principal.groupby('Resultado')['Variacao_rs'].sum().reset_index()
#print(df_analise_saldo) - Soma agrupada por saldo

fig = px.bar(df_analise_saldo, x='Resultado', y='Variacao_rs', text='Variacao_rs', title='Variação Reais por Resultado')
#fig.write_image('figura.png') - Criando o gráfico de saldo

