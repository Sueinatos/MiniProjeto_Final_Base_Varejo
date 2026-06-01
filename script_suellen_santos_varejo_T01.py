#Script para Análise de Dados da Base Varejo

#1.IMPORTANTO BIBLIOTECAS 

import pandas as pd #Processamento de dataframe
import numpy as np #Cálculos numéricos 
from datetime import datetime #Operações com datas

#2.CARREGAMENTO DOS DADOS BRUTOS PARA ANÁLISE

caminho=r'C:\MiniProjeto_Final_Suellen_Santos_T01\Base Varejo.csv'

#Transformando em DataFrame
df_dados=pd.read_csv(caminho,sep=';')
print("="*40)

#3.ANÁLISE EXPLORATÓRIA 

#Números de linhas antes da limpeza
total_original=len(df_dados)
print (f'Linhas ANTES da LIMPEZA:',(total_original))
print("="*40)

print("____________"'CABEÇALHO'"____________")
print(df_dados.head())#Mostrar as primeiras 05 linhas do dataframe
print("="*40)

print("____________"'INFORMAÇÕES'"____________")
print(df_dados.info()) #Identificar os números de colunas e linhas
print("="*40)

#Localizar valores nulos por coluna
print("Valores NULOS por coluna")
print(df_dados.isnull().sum())
print("="*40) #Foram encontrados campos com NaN devido a colunas unnamed 

#Localizar duplicados
print("Valores Duplicados")
print(df_dados[df_dados.duplicated()]) #Campos com NaN devido a colunas unnames

#Visualizar valores únicos nas colunas 
print("Valores ÚNICOS por coluna")
def valores_unicos(df): 
    colunas_unicos = ['DATA','CL_GENERO', 'CL_EC', 'CL_FHL', 'CL_SEG', 'PR_NOME', 'PR_CAT']

    for col in colunas_unicos:
        print(f'\n{col}:')
        print(df[col].dropna().unique().tolist())

valores_unicos(df_dados)
print("="*40)

#Analise descritiva da coluna "CL_FHL"
print("Análise da coluna CL_FHL")
print('Número de linhas:',df_dados['CL_FHL'].count())
print('Valor maximo:',df_dados['CL_FHL'].max())
print('Valor minimo:',df_dados['CL_FHL'].min())
print('Valor média:',df_dados['CL_FHL'].mean())
print('Valor desvio padrão:',df_dados['CL_FHL'].std())
print('Valor mediana:',df_dados['CL_FHL'].median())
print('Valor moda:',df_dados['CL_FHL'].mode())
print("="*40)

#4.APLICAÇÃO DAS REGRAS DE LIMPEZA

#Remoção de colunas vazias
#Padronização de textos e datas
#Tratamento de valores nulos

#Remoção de colunas unnammed
print('Remoção das colunas Unnamed')
df_dados = df_dados.dropna(axis=1,how='all')
print("="*40)

#Padronização de texto 
print('Padronização de texto')
def padronizar_campos_texto(df): #Remover espaços extras e colocar tudo em maiusculo 
    for col in ['PR_CAT','PR_NOME']:
        df[col]=df[col].astype(str).str.strip().str.upper()
    return df
df_dados=padronizar_campos_texto(df_dados)
print("="*40)

#Conversão de data para datatime
print('Convertendo STR para DATETIME')
def padronizar_datas(df):
    df['DATA']=pd.to_datetime(df['DATA'],errors='coerce')
    df=df.dropna(subset=['DATA'])
    return df
df_dados=padronizar_datas(df_dados)
print("="*40)

#Tratamento de Nulos 
print('Convertendo #N/D para NaN')
df_dados[['PR_CAT','PR_NOME']]=df_dados[['PR_CAT','PR_NOME']].replace('#N/D',np.nan)

#Preenchendo dados NaN para SEM CATEGORIA
df_dados[['PR_CAT','PR_NOME']]= df_dados[['PR_CAT','PR_NOME']].fillna('SEM CATEGORIA')
print("="*40)

#5.CRIAÇÃO DE AGRUPMAENTO DE COLUNAS

#Relacionando dados de quem comprou fraldas e quantidade de filhos com groupby
print('Relacionando colunas CL_FHL, CL_GENERO e PR_NOME')
def genero_fralda_filhos(df):
    df = df.copy()
    
    #Indicador de compra de fralda
    df['comprou_fralda'] = df['PR_NOME'].str.contains('fralda', case=False, na=False)
    
    #Filtrando apenas quem comprou fralda
    df_fralda = df[df['comprou_fralda']]
    
    #Agrupamento por gênero e quantidade de filhos
    resultado = (
        df_fralda
        .groupby(['CL_GENERO','CL_FHL'])
        .size()
        .reset_index(name='QUANTIDADE')
        .sort_values(by='QUANTIDADE', ascending=False)
        .reset_index(drop=True)
    )
    return resultado
print(genero_fralda_filhos(df_dados))
print("="*40)

#Relacionando a classe com categoria com groupby
print('Relacionando colunas CL_SEG e PR_CAT')
def categorias_por_classe(df):
    df = df.copy()
    
    resultado = (
        df
        .groupby(['CL_SEG', 'PR_CAT'])
        .size()
        .reset_index(name='QUANTIDADE')
        .sort_values(['CL_SEG', 'QUANTIDADE'], ascending=[True, False])
        .reset_index(drop=True)
    )
    return resultado
print(categorias_por_classe(df_dados))
print("="*40)


#Contadores do relatório final
def relatorio_final(df):
    df = df.copy()
    
    print("="*40)
    print("RELATÓRIO FINAL")
    print("="*40)
    
    #Distribuição por gênero
    print("Compras por gênero:")
    print(df['CL_GENERO'].value_counts())
    print("="*40)
    #Distribuição por filhos
    print(" Quantidade de filhos:")
    print(df['CL_FHL'].value_counts().sort_index())
    print("="*40)
    #Produto mais vendido
    print(" Produto mais vendido:")
    print(df['PR_NOME'].value_counts().head(1))
    print("="*40)
    #Categoria mais vendida
    print("Categoria mais vendida:")
    print(df['PR_CAT'].value_counts().head(1))
    print("="*40)
relatorio_final(df_dados)

print("Exportanto a base limpa")

#Salvando os dados limpos 
df_dados.to_csv('df_limpo_suellen_T01.csv', sep=';', index=False, encoding='utf-8')