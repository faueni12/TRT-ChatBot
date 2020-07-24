""" Principal do projeto. Aqui onde é executado todas as funções
e análises. """
# -*- coding: UTF-8 -*- 
import pandas as pd
import time

import settings
import Analysis

df = pd.read_excel("csv/Histórico dos Chamados.xlsx")

df_categorias_mais_frequentes = df["CATEGORIA"].value_counts()
df_servicos_mais_frequentes = df["SERVICO"].value_counts()
df_servicos_mais_frequentes.to_csv('csv/serviços mais frequentes.csv', encoding='utf-8')

# Analisar as descrições dos top 10 serviços da categoria
# Solucionar incidente (falha ou baixo desempenho)
dfCategoria = df[df["CATEGORIA"] == "Solucionar incidente (falha ou baixo desempenho)"]
servicos = dfCategoria["SERVICO"].value_counts().index
for i in range(10):
    # Pegar descricao por serviço por categoria
    descriptions = dfCategoria[dfCategoria["SERVICO"] == servicos[i]]["DESCRICAO"]
    Analise = Analysis.Analysis(descriptions)

    # Obter tokens mais frequentes e Salvá-los em DataFrame
    # Pegar nome do serviço e corrigir Bug ao salvar nome de arquivo com / no nome
    servico = servicos[i].replace('/', '|')
    nameDf = 'csv/Tokens - SIFBD - '+servico+'.csv'
    Analise.getFrequentTokens(nameToSave=nameDf)

    # Gerar descrições que contiver 3 tokens, no minimo
    goodDescripts = [Analise.analizeDescription(description, nameDf, 3)
                     for description in descriptions]
    goodDescripts = [x for x in goodDescripts if x != None]

    # Retirar alguns simbolos das descrições
    greatDescripts = Analise.removeBadSimbols(goodDescripts,
        settings.simbols, simbols2=settings.simbols)
    # E também tags html / javascript
    greatDescripts = Analise.removeTags_(greatDescripts)

    # Salvar as descrições em csv
    dfDescript = pd.Series(greatDescripts)
    nameDf = "csv/Descrições - SIFBD - "+servico+".csv"
    dfDescript.to_csv(nameDf, encoding='utf-8')

for i in greatDescripts:
    print(i)
    time.sleep(0.8)