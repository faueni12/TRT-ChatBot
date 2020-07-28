""" Principal do projeto. Aqui onde é executado todas as funções
e análises. """
# -*- coding: UTF-8 -*- 
import os
import pandas as pd

import settings
import Analysis

df = pd.read_excel("csv/Histórico dos Chamados.xlsx")

# Mudar nome das categorias e serviços pra evitar bug de diretório
df["CATEGORIA"] = [cat.replace("/", "|") for cat in df["CATEGORIA"]]
df["SERVICO"] = [str(cat).replace("/", "|") for cat in df["SERVICO"]]
 
df_categorias_mais_frequentes = df["CATEGORIA"].value_counts()
df_servicos_mais_frequentes = df["SERVICO"].value_counts()
df_servicos_mais_frequentes.to_csv('csv/serviços mais frequentes.csv', encoding='utf-8')

# Analisar as descrições dos top 10 serviços das top 2 categorias
categorias = df["CATEGORIA"].value_counts().index
totalAntes, totalDepois = {}, {}
for categoria in categorias[:1]:
    dfCategoria = df[df["CATEGORIA"] == categoria]
    servicos = dfCategoria["SERVICO"].value_counts().index

    qtDescricao = {}
    for servico in servicos[:10]:
        # Pegar descricao por serviço por categoria
        descriptions = dfCategoria[dfCategoria["SERVICO"] == servico]["DESCRICAO"]
        Analise = Analysis.Analysis(descriptions)

        # Contar quantas descrições tinha antes, a fim de cálculos
        qtDescricao[servico] = [descriptions.size]

        # Obter tokens mais frequentes e Salvá-los em DataFrame
        nameDf = f"csv/{categoria}/Tokens/{servico}.csv"
        if not os.path.exists(os.path.dirname(nameDf)):
                os.makedirs(os.path.dirname(nameDf))
        Analise.getFrequentTokens(nameToSave=nameDf)

        # Gerar descrições que contiver 3 tokens, no minimo
        goodDescripts = [Analise.analizeDescription(description, nameDf, 3)
                        for description in descriptions]
        goodDescripts = [x for x in goodDescripts if x != None]

        # Retirar alguns simbolos das descrições
        greatDescripts = Analise.removeBadSimbols(goodDescripts,
            settings.simbols, simbols2=settings.simbols2)
        # E também tags html / javascript
        greatDescripts = Analise.removeTags_(greatDescripts)

        # Salvar as descrições em csv
        dfDescript = pd.Series(greatDescripts)
        nameDf = f"csv/{categoria}/Descrições/{servico}.csv"
        if not os.path.exists(os.path.dirname(nameDf)):
                os.makedirs(os.path.dirname(nameDf))
        dfDescript.to_csv(nameDf, encoding='utf-8')

        # Contar quantas descrições boas foram pegas e a porcentagem em relação ao total
        qtDescricao[servico] += [len(greatDescripts), 100*len(greatDescripts) / qtDescricao[servico][-1]]

    totalAntes[categoria] = sum([x[0] for x in qtDescricao.values()])
    totalDepois[categoria] = sum([x[1] for x in qtDescricao.values()])

