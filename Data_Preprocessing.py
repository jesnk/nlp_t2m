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


## Pos Tagging and estract

def extractNouns(tokens):
    tagged_list = nltk.pos_tag(tokens)
    nouns_list = [t[0] for t in tagged_list if t[1] == "NN"]
    return nouns_list

def extractVerbs(tokens):
    tagged_list = nltk.pos_tag(tokens)
    verbs_list = [t[0] for t in tagged_list if t[1] == "VB"]
    return verbs_list


#nltk.download()

## Indexing

## Word Indexing & Preprocessing in all the in data dir



# 훈련 데이터 인덱싱
def indexingScripts(path_trainDataDir) :
    genre_list = os.listdir(path_trainDataDir)
    total_freq = []

    for i in genre_list[:]:
        print("Indexing Train Data, Genre : %s" % i )
        path_file = path_trainDataDir+'/'+i+'/'
        file_list = os.listdir(path_file)
        data = ""
        for j in file_list[:]:
            if not (j[-4:] == ".txt") :
                continue
            print("Indexing : %s " % j)
            f = open(path_file+j,'rt', encoding='utf-8')
            data = data + f.read()
        print("processing... %s" % i)
        preprocessed = preprocessing(data)
        fdist=FreqDist(preprocessed)
        freq = [i, fdist.most_common(100)]
        total_freq += [freq]
        print(freq,'\n')
    
    return total_freq


# 테스트 쿼리 인덱싱
def indexingTestFiles(path_input) :
    file_list = os.listdir(path_input) 
    ret_list = [] 
    for f in file_list[:] :
        if not (f[-4:] == ".txt") :
            continue

        t = open(path_input+"/"+f, 'rt', encoding = 'utf-8') 
        text = t.read()
        preprocessed = preprocessing(text)
        fdist = FreqDist(preprocessed)
        # 100개 단어를 추린다. 
        freq = [ f[:-4] , fdist.most_common(100)]
        ret_list.append(freq)
    return ret_list 



def queryProcessing(text,name) :
    data = text
    preprocessed = preprocessing(data)
    fdist = FreqDist(preprocessed)

    freq = [name, fdist.most_common(300)]
    return freq

