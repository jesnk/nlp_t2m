#from testModel import *
from glob import *
import pickle
from Data_Preprocessing import *
import matplotlib.pyplot as plt
import numpy as np

class DataReposit :
    #dataset = []
    indexedSet = []
    modelFrame = []
    modelSet = []
    queryModel = []

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

    def showModel(self) :
        x = [i[0] for i in self.modelSet[0][1][:]]
        y = [i[1] for i in self.modelSet[0][1][:]]
        fig = plt.figure()
        ax0 = fig.add_subplot(2,3,1)
        
        ax0.plot(x,y)
        
        x = [i[0] for i in self.modelSet[1][1][:]]
        y = [i[1] for i in self.modelSet[1][1][:]]

        ax1 = fig.add_subplot(2,3,2)
        ax1.bar(x,y, width = 1.0)
        ax1.set_title('%s' % self.modelSet[1][0])
        ax1.xaxis.set_major_formatter(plt.NullFormatter())
        #ax1.yaxis.set_major_locator(plt.NullLocator())
        ax1.set_xlabel("Term")
        ax1.set_ylabel("Freq")


        axQ = fig.add_subplot(2,3,3)
        x = [i[0] for i in self.queryModel[0][1][:]]
        y = [i[1] for i in self.queryModel[0][1][:]]
        axQ.bar(x,y, width = 1.0)
        axQ.set_title('%s' % self.queryModel[0][0])
        #axQ.xaxis.set_major_formatter(plt.NullFormatter())


        plt.show()



def query(modelFrame) :
    print("input name of script")
    nameBuf = input()
    text = textFileImport(nameBuf)
    if text == '' :
        print("There is not %s" % nameBuf)
        return False
    print("There is %s" % nameBuf)

    indexedQuery = queryProcessing(text,nameBuf)
    queryModel = makeModel_query(indexedQuery, modelFrame)
    return queryModel


def makeModel_query(indexedQuery, modelFrame) :
    
    tmpModel = [ indexedQuery[0], modelFrame[:] ]
    for word in indexedQuery[1] :
        # word : ( term, tf )
        if [word[0],0] in tmpModel[1] :
            tmpIdx = tmpModel[1].index([word[0],0])
            tmpModel[1][tmpIdx] = [word[0], word[1]]
    return tmpModel
    
def textFileImport(name) :
    if not (glob("./input/%s.txt" % name)) :
        return False
    else : 
        f = open("./input/%s.txt" % name, 'rt', encoding = 'utf-8')
        text = f.read()
        return text







'''
def textFileImport(genre) :
    scripts = []
    for textFile in glob("./data/%s/*.txt" % genre) :
        scripts.append(textFile)
    return scripts
'''




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


while (True) :
    queryBuf = query(dataSource.modelFrame)
    if not queryBuf :
        continue
    else :
        dataSource.queryModel.append(queryBuf)
        dataSource.showModel()

dataSource.showModel()





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
