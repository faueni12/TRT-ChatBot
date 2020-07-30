""" Nesse arquivo tem as funções de limpar texto e de análise. 
Limpa textos, pega tokens, faz nuvens de palavras"""
# -*- coding: UTF-8 -*- 
import re, string

import settings

def cleanTextPart1(text):     
    """ Transformar em minúsculo, retirar o que tiver entre colchetes e tags html/javascript,
    remover pontuação e números """                              
    #text = str.lower(str(text))
    text = re.sub('\[.*?\]', '', text)
    text = removeTextInTags(text)
    text = re.sub('[%s]' % string.punctuation, '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

def removeTextInTags(text):
    """ Remove tudo dentro das tags """
    from bs4 import BeautifulSoup
    return BeautifulSoup(text, "html.parser").text

def getFrequentTokens(df, quantity=150):
    """ Obter tokens da descrição, remover stopwords e pegar os tokens mais frequentes 
    que tiverem frequencia maior que 180 """
    from nltk.probability import FreqDist
    from nltk.tokenize import word_tokenize
    tokens = []
    for phrase in df:
        tokens += word_tokenize(phrase)
    tokens = [token for token in tokens if token not in settings.STOP_WORDS]
    tokens = FreqDist(tokens).most_common(quantity)
    tokens = [token for token in tokens if token[1] > 180]
    return tokens

def makeWordCloud(df, stopwords, title):
    """ Fazer uma nuvem de palavras eliminando as stopwords. Você pode passar um ou mais dfs,
    contanto que seja passada uma lista. Em seguida mostra as nuvens de todos os DataFrames"""
    import matplotlib.pyplot as plt
    plt.rcParams['figure.figsize'] = [16, 6]
    
    from wordcloud import WordCloud
    wordCloud = WordCloud(stopwords=stopwords, background_color="white", colormap="Dark2",
                          max_font_size=150, random_state=42)
    
    for index, df in enumerate(df):
        allText = " ".join(s for s in df)
        wordCloud.generate(allText)
        
        plt.subplot(3, 4, index+1)
        plt.imshow(wordCloud, interpolation="bilinear")
        plt.axis("off")
        plt.title(title[index])
    
    plt.savefig("png/Tokens - SIFDB - Top 10 serviços.png")
    plt.show()
