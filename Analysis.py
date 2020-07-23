""" Classe das funções de análise. Aqui pegará as palavras-chave,
e as descrições que as conterem (apenas uma parte delas, de forma resumida)"""
# -*- coding: UTF-8 -*- 
import pandas as pd

from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize

import settings

class Analysis:
    def __init__(self, df):
        self.df = df
        self.df_tokens = {}

    """ A função vai pegar todas as palavras mais frequentes, retornando
    um DataFrame com o argumento "nameToSave"
    """
    def getFrequentTokens(self, quantity=150, **kwargs):
        # Obter tokens da descrição
        tokens = []
        for frase in self.df.apply(lambda phrase: str.lower(str(phrase))):
            tokens += word_tokenize(frase)

        # Remover stopwords
        tokens = [token for token in tokens if token not in settings.stop_words]

        # Tokens mais frequentes
        freqTokens = FreqDist(tokens).most_common(quantity)
        
        # Salvá-los em csv se tiver o argumento "nameToSave"
        nameDf = kwargs.get("nameToSave")
        if nameDf:
            word = [w[0] for w in freqTokens]
            quantity = [q[1] for q in freqTokens]
            df = pd.DataFrame({'word':word, 'quantity':quantity})
            df.to_csv(nameDf, encoding="utf-8")

            # Guardar os dataFrames pra melhorar o desempenho da proxima função
            self.df_tokens[nameDf] = df

        return freqTokens

    """ Pegará as descrições que tiverem um numero de ocorrencias de tokens """
    def analyzeDescription(self, description, nameDfTokens, occurrences, separator='.', quantity=150):
        tokens = self.df_tokens[nameDfTokens]["word"][:quantity]
        # Acessar cada frase separada por um separador (por padrão, "."),
        # pra resumir as descrições. Vai pegar a primeira que tiver esse numero de ocorrencias
        for descript in str.lower(description).split(separator):
            # contar quantas ocorrencias de tokens na frase
            occurrencesTokens = [descript.count(str(token)) for token in tokens]
            qtTokens = len([occur for occur in occurrencesTokens if occur > 0])
            if qtTokens >= occurrences:
                return descript
