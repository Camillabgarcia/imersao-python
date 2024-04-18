import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import mplfinance as yf
import plotly.graph_objects as go
import yfinance as yf
from plotly.subplots import make_subplots
from matplotlib.patches import Rectangle


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
#fig.write_image('figura.png') - Criando o gráfico de saldo em relação a resultado e variação

dados = yf.download('PETR4.SA', start='2023-01-01', end='2023-12-31')
#print(dados) Puxando os dados da Petrobras do ano de 2023

dados.columns = ['Abertura', 'Maximo', 'Minimo', 'Fechamento', 'Fech_Ajust', 'Volume']
#print(dados.columns) - Renomeando as colunas em Portugues 

dados = dados.rename_axis('Data')
#print(dados)

dados['Fechamento'].plot(figsize=(10,6))
#plt.show() - Criando imagem da Petrobras do ano de 2023

dados['Fechamento'].plot(figsize=(10,6))
#plt.title('Variação do preço por data', fontsize=16)
#plt.legend(['Fechamento'])
#plt.show()

df = dados.head(60).copy()
#print(df) - Mostrando as 60 primeiras linhas do dataframe

#Convertendo o indice em uma coluna de data
df['Data'] = df.index
#print(df)

#Convertendo as datas para o formato numérico de matplotlib
#Isso é necessário para que o Matplotlib possa plotar as datas corretamente no gráfico
df['Data'] = df['Data'].apply(mdates.date2num)
#print(df)

fig, ax = plt.subplots(figsize=(15, 8))
width = 0.7

for i in range(len(df)):
    if df['Fechamento'].iloc[i] > df['Abertura'].iloc[i]:
        color = 'green'
    else:
        color = 'red'

    # Corrigindo a chamada para ax.plot
    ax.plot([df['Data'].iloc[i], df['Data'].iloc[i]],
            [df['Minimo'].iloc[i], df['Maximo'].iloc[i]],  # Corrigindo a vírgula aqui
            color=color,
            linewidth=1)

    # Corrigindo a chamada para ax.add_patch e utilizando a classe Rectangle diretamente
    ax.add_patch(Rectangle((df['Data'].iloc[i] - width/2, min(df['Abertura'].iloc[i], df['Fechamento'].iloc[i])),
                           width,
                           abs(df['Fechamento'].iloc[i] - df['Abertura'].iloc[i]),
                           facecolor=color))

df['MA7'] = df['Fechamento'].rolling(window=7).mean()
df['MA14'] = df['Fechamento'].rolling(window=14).mean()

ax.plot(df['Data'], df['MA7'], color='orange', label='Média Móvel 7 Dias')
ax.plot(df['Data'], df['MA14'], color='yellow', label='Média Móvel 14 Dias')
ax.legend()

ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)

plt.title('Gráfico de Candlestick - PETR4.SA com matplotlib')
plt.xlabel('Data')
plt.ylabel('Preço')

plt.grid(True)

#plt.show()

# Criando subplots
'''
"Primeiro, criamos uma figura que conterá nossos gráficos usando make_subplots.
Isso nos permite ter múltiplos gráficos em uma única visualização.
Aqui, teremos dois subplots: um para o gráfico de candlestick e outro para o volume de transações."

'''
fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.1,
                    subplot_titles=('Candlesticks', 'Volume Transacionado'),
                    row_width=[0.2, 0.7])

'''
"No gráfico de candlestick, cada candle representa um dia de negociação,
mostrando o preço de abertura, fechamento, máximo e mínimo. Vamos adicionar este gráfico à nossa figura."
'''
# Adicionando o gráfico de candlestick
fig.add_trace(go.Candlestick(x=df.index,
                             open=df['Abertura'],
                             high=df['Maximo'],
                             low=df['Minimo'],
                             close=df['Fechamento'],
                             name='Candlestick'),
                             row=1, col=1)

# Adicionando as médias móveis
# Adicionamos também médias móveis ao mesmo subplot para análise de tendências
fig.add_trace(go.Scatter(x=df.index,
                         y=df['MA7'],
                         mode='lines',
                         name='MA7 - Média Móvel 7 Dias'),
                         row=1, col=1)

fig.add_trace(go.Scatter(x=df.index,
                         y=df['MA14'],
                         mode='lines',
                         name='MA14 - Média Móvel 14 Dias'),
                         row=1, col=1)

# Adicionando o gráfico de barras para o volume
# Em seguida, criamos um gráfico de barras para o volume de transações, que nos dá uma ideia da atividade de negociação naquele dia
fig.add_trace(go.Bar(x=df.index,
                     y=df['Volume'],
                     name='Volume'),
                     row=2, col=1)

# Atualizando layout
#Finalmente, configuramos o layout da figura, ajustando títulos, formatos de eixo e outras configurações para tornar o gráfico claro e legível.
fig.update_layout(yaxis_title='Preço',
                  xaxis_rangeslider_visible=False,  # Desativa o range slider
                  width=1100, height=600)

# Mostrando o gráfico
#fig.show()

dados = yf.download('AAPL', start='2023-01-01', end='2023-12-31')
mpf.plot(dados.head(30), type='candle', figsize = (16,8), volume=True, mav=(7,14))
#plt.show()