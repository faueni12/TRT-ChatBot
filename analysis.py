""" Nesse arquivo tem as funções de limpar texto e de análise. 
Limpa textos, pega tokens, faz nuvens de palavras"""
# -*- coding: UTF-8 -*- 
import re, string
import matplotlib.pyplot as plt
    
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

def getFrequentTokens(df, stopwords, quantity=30, **kwargs):
    """ Obter tokens da descrição, remover stopwords e pegar os tokens mais frequentes
    por quantidade {quantity}; OU se tiverem frequencia maior que {maiorQue} (kwargs). """
    from nltk.probability import FreqDist
    from nltk.tokenize import word_tokenize
    tokens = []
    for phrase in df:
        tokens += word_tokenize(phrase)
    tokens = [token for token in tokens if token not in stopwords]
    tokens = FreqDist(tokens).most_common(quantity)
    
    maiorQue = kwargs.get('maiorQue')
    if maiorQue:
        tokens = [token for token in tokens if token[1] > maiorQue]
    
    return tokens

def makeWordCloud(df, stopwords, title):
    """ Fazer uma nuvem de palavras eliminando as stopwords. Você pode passar um ou mais dfs,
    contanto que seja passada uma lista. Em seguida mostra as nuvens de todos os DataFrames"""
    from wordcloud import WordCloud
    wordCloud = WordCloud(stopwords=stopwords, background_color="white", colormap="Dark2",
                          max_font_size=150, random_state=42, height=300)
    
    for index, df in enumerate(df):
        allText = " ".join(s for s in df)
        wordCloud.generate(allText)
        
        plt.subplot(3, 3, index+1)
        plt.imshow(wordCloud, interpolation="bilinear")
        plt.axis("off")
        plt.title(title[index])
    
    plt.savefig("png/Tokens/SIFBD/Top 9 serviços.png")
    plt.show()
    
def makeWordStrippBar(title, commonWords, countCommonWords):
    """ Faz um gráfico com as palavras mais usadas, pra ter uma melhor ideia dos números """
    plt.tight_layout()
    
    import seaborn as sns
    graph = sns.stripplot(x=commonWords, y=countCommonWords)
    graph.set(xlabel ='Palavras (%d)'%(len(commonWords)),
              ylabel ='Frequência') 
    graph.set_xticklabels(graph.get_xticklabels(), rotation=83)
    plt.title(title)
    plt.savefig(f"png/Tokens/SIFBD/{title}.png")
    plt.show()