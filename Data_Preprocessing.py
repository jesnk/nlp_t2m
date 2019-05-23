# -*- coding: utf-8 -*-

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import Text
from nltk import FreqDist
import os

## Data Preprocessing
def preprocessing(text):
    # 1.Tokenize into words
    tokens = [word for sent in nltk.sent_tokenize(text)
              for word in nltk.word_tokenize(sent)]

    # 2.Cleaning : Remove words less than three letters & Lower capitalization & Remove Numbers
    tokens = [word.lower() for word in tokens if len(word) >= 3  if not word.isdigit()]
    
    # 3.Remove stopwords
    stop = stopwords.words('english')
    stop.extend(["n't","'re","i'm","'ve",'...'])
    tokens = [token for token in tokens if token not in stop]
    
    # 4.Lemmatization
    lmtzr = WordNetLemmatizer()
    tokens = [lmtzr.lemmatize(word) for word in tokens]
    tokens = [lmtzr.lemmatize(word, 'v') for word in tokens]

    return tokens

    
#nltk.download()

## Indexing

## Word Indexing & Preprocessing in all the in data dir


def indexingScripts() :
    path_genre = './data/'
    genre_list = os.listdir(path_genre)
    total_freq = []
    for i in genre_list[:]:
        path_file = path_genre+i+'/'
        file_list = os.listdir(path_file)
        data = ""
        for j in file_list[:]:
            if not (j[-4:] == ".txt") :
                continue
            print("Indexing... ",j)
            f = open(path_file+j,'rt', encoding='utf-8')
            data = data + f.read()
        print("processing... %s" % i)
        preprocessed = preprocessing(data)
        fdist=FreqDist(preprocessed)
        freq = [i, fdist.most_common(100)]
        total_freq += [freq]
        print(freq,'\n')
    
    return total_freq

def queryProcessing(text,name) :
    data = text
    preprocessed = preprocessing(data)
    fdist = FreqDist(preprocessed)

    freq = [name, fdist.most_common(100)]
    return freq

