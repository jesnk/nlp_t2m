

# Team T2M
# S/S, 2019 Natural Language Processing & Information Retrival

# Project Subject : Movie Genre Classification by Script
# github link : https://github.com/jesn1219/nlp_t2m



from glob import *
import pickle
from Data_Preprocessing import *
import matplotlib.pyplot as plt
import numpy as np


# Class for Store data
class DataReposit :
    # indexed data : [ ['Genre', ['Title', [ 
    indexedSet = []
    modelFrame = []
    modelSet = []
    queryModel = []

    # Constructor
    def __init__(self) :
        print("DataReposit Object init")
    
    def indexing(self) :
        self.indexedSet = indexingScripts()
    def createModelFrame(self) :
        self.modelFrame = []
        for g in self.indexedSet :
            # g : ['Genre Name', [ (term, tf), (term2, tf), ........ ]]
            for t in g[1] :
                # t : (term, tf)
                if [t[0],0] in self.modelFrame :
                    continue
                else :
                    self.modelFrame.append([t[0], 0])
    
    def makeModel(self) :
        for g in self.indexedSet :
            # g : ['Genre Name', [ (term, tf), (term2, tf), ..... ]
            
            # init genre Model using modelFrame
            tmpModel = [ g[0], self.modelFrame[:] ]
            for word in g[1] :
                # word : ( term, tf )
                if [word[0],0] in tmpModel[1] :
                    tmpIdx = tmpModel[1].index([word[0],0])
                    tmpModel[1][tmpIdx] = [word[0], word[1]]
            self.modelSet.append(tmpModel)
    def scaleModelSet(self) :
        modelScaler(self.modelSet,1000)
    def predictGenre(self) :
        genreDistance = []
        for g in self.modelSet :
            tmp = calModelDistance(g,self.queryModel[0])
            genreDistance.append( [g[0], tmp] )
        ret = sorted(genreDistance, key = lambda i : i[1], reverse = False)
        print(ret)


    def showModel(self,isQ) :
        fig = plt.figure()
        tmp_idx = 1
        for model in self.modelSet :
            x = [ i[0] for i in model[1][:]]
            y = [ i[1] for i in model[1][:]]
            ax_tmp = fig.add_subplot(6,5,tmp_idx)
            ax_tmp.bar(x,y, width = 1.0, color = 'Grey')
            ax_tmp.set_title("%s" % model[0])
            ax_tmp.set
            #ax_tmp.set_xlabel("Term")
            #ax_tmp.set_ylabel("Freq")
            ax_tmp.xaxis.set_major_formatter(plt.NullFormatter())
            #ax_tmp.yaxis.set_major_locator(plt.NullLocator())
            tmp_idx += 1
        if isQ :
            axQ = fig.add_subplot(6,5,tmp_idx)
            x = [i[0] for i in self.queryModel[0][1][:]]
            y = [i[1] for i in self.queryModel[0][1][:]]
            axQ.bar(x,y, width = 1.0, color = "red")
            axQ.set_title('Query : %s' % self.queryModel[0][0])
            axQ.xaxis.set_major_formatter(plt.NullFormatter())
            #axQ.yaxis.set_major_locator(plt.NullLocator())
            
        plt.subplots_adjust(hspace = 1.0, wspace = 0.1)
        plt.show()
    

def modelScaler(modelSet,scale) :
    total_tf = 0
    for model in modelSet :
        total_tf = 0
        #Calculate total_tf
        for term in model[1] :
            total_tf += term[1]
        
        for term in model[1] :
            term[1] = term[1] * 100/total_tf


def query(modelFrame) :
    print("input name of script")
    nameBuf = input()
    if nameBuf == 'show' :
        dataSource.showModel(True)
        return False
    text = textFileImport(nameBuf)
    if text == '' :
        print("There is not %s" % nameBuf)
        return False
    print("There is %s" % nameBuf)

    indexedQuery = queryProcessing(text,nameBuf)
    queryModel = makeModel_query(indexedQuery, modelFrame)
    return queryModel

def calModelDistance(genre, query) :
    # genre : [ 'title', [ [term,tf], [term, tf] .. ]]
    total_Distance = 0
    for idx in range(0, len(genre)) :
        total_Distance +=  np.square(genre[1][idx][1] - query[1][idx][1])
    return total_Distance

def makeModel_query(indexedQuery, modelFrame) :
    
    tmpModel = [ indexedQuery[0], modelFrame[:] ]
    for word in indexedQuery[1] :
        # word : ( term, tf )
        if [word[0],0] in tmpModel[1] :
            tmpIdx = tmpModel[1].index([word[0],0])
            tmpModel[1][tmpIdx] = [word[0], word[1]]
    modelScaler([tmpModel],1000)

    return tmpModel
    
def textFileImport(name) :
    if not (glob("./input/%s.txt" % name)) :
        return False
    else : 
        f = open("./input/%s.txt" % name, 'rt', encoding = 'utf-8')
        text = f.read()
        return text



print("Hello")
makeNewIndexData = False 
dataSource = DataReposit()

if makeNewIndexData :
    dataSource = DataReposit()
    dataSource.indexing()
    dataSource.createModelFrame()
    dataSource.makeModel()
    with open("indexedModel.t2m", "wb") as file :
        pickle.dump(dataSource, file)
        print("Model Saved")
    

if not makeNewIndexData :
    with open("indexedModel.t2m", "rb") as file :
        dataSource = pickle.load(file)
        dataSource.makeModel()
    

dataSource.scaleModelSet()
#dataSource.showModel(False)


while (True) :
    queryBuf = query(dataSource.modelFrame)
    if not queryBuf :
        continue
    else :
        dataSource.queryModel = [queryBuf]
        dataSource.predictGenre()
        #dataSource.showModel(True)




'''
def textFileImport(genre) :
    scripts = []
    for textFile in glob("./data/%s/*.txt" % genre) :
        scripts.append(textFile)
    return scripts
'''





### Load Indexed Data or Do Indexing
'''
if makeNewIndexData :
    with open("indexedModel.t2m", "wb") as file :
        pickle.dump(dataSource, file)
    print("Index saved")
else :
    with open("indexedModel.t2m", "rb") as file :
        dataSource = pickle.load(file)
'''





'''                


def detectGenres() :
    Genres = []
    for dir in glob("./data/*") :
        Genres.append(dir[7:])
    return Genres  

def dataImport() :
    dataset = []
    Genres = detectGenres()
    for genre in Genres :
        data = textFileImport(genre)
        dataset.append([genre, data])    
    return dataset
'''
'''
def makeVSM(entireWordDics) :
    resultVSM = []
    numOfD = len(entireWordDics)
    
    # Calculate tf, stored in resultVSM temporary
    for idxD in range(0,numOfD) :
        selectedD = entireWordDics[idxD]
        for term in selectedD :
            if not (term in termsInfo) :
                termsInfo.append(term)
                resultVSM.append([])
                for i in range(0,numOfD) :
                    resultVSM[termsInfo.index(term)].append(0)
                
                resultVSM[termsInfo.index(term)][idxD] = selectedD[term]
            else :
                resultVSM[termsInfo.index(term)][idxD] = selectedD[term]

    # tf - idf calculate
    for term in resultVSM :
        df = 0
        for tfIdx in range(0, len(entireWordDics) ) :
            if term[tfIdx] != 0 :
                df = df + 1
        
        idf = df / ( 1 + len(entireWordDics) )
        #idf = math.log(2,idf)
        globalDfInfo.append(df)
    
        for tfIdx in range(0, len(entireWordDics) ) :
            if term[tfIdx] != 0 :
                term[tfIdx] = term[tfIdx]*idf
    
    print("END makeVSM")        
    return resultVSM

'''
