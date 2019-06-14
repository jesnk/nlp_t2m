import main
import pickle
import Data_Preprocessing
import matplotlib as plt
import numpy as np 
import os 
from excel_write import *
import math 





import Data_Preprocessing
class TrainData :
    def __init__(self, path_trainDataDir) :
        self.path_trainDataDir = path_trainDataDir

    def indexScripts(self,path_trainDataDir) :
        self.indexSet = Data_Preprocessing.indexingScripts(path_trainDataDir)
        
    def saveIndexData(self) :
        with open("model.t2m", "wb") as file :
            pickle.dump(self.indexSet,file)
            print("Index Data is Saved")
    def loadIndexData(self,path_modelDataDir,num) :
        with open(path_modelDataDir+"/model_"+str(num)+".t2m", "rb") as file :
            self.indexSet = pickle.load(file)
            print("Index Data is loaded")
    def getIndexData(self) :
        return self.indexSet
class Model :
    def __init__(self) :
        print("Model Object Created")
        self.indexSet = []
    def createFrame(self) :
        self.frame = []
        for g in self.indexSet :
            for t in g[1] :
                if [t[0],0] in self.frame :
                    continue
                else :
                    self.frame.append([t[0], 0])
    
    def createGenreModel(self,isScale) :
        self.genreModel = []
        print("Creating Genre Model")
        self.df = {}
        for g in self.indexSet :
            tmpModel = [ g[0], self.frame[:] ]
            for word in g[1] :
                if [word[0],0] in tmpModel[1] : 
                    tmpIdx = tmpModel[1].index([word[0],0])
                    tmpModel[1][tmpIdx] = [word[0], word[1]]

                    if word[0] in self.df.keys() :
                        self.df[word[0]] += 1
                    else :
                        self.df[word[0]] = 1
            self.genreModel.append(tmpModel)
        self.createIdf()
        print("Complete Creating Genre Model")
    def init(self,indexData) :
        self.importIndexData(indexData)

    def importIndexData(self,indexData) :
        self.indexSet = indexData.getIndexData()

    def createIdf(self) :
        print("Creating idf Dictionary")
        #assert(self.genreModel == [])
        self.idf = {}
        numOfD = len(self.genreModel)
        for term in self.df :
            self.idf[term] = math.log(1 + self.df[term],2)
            self.idf[term] = numOfD / self.idf[term]
        print("Complete Creating idf Dictionary")
    
    def applyingScalingToGenreModel(self,size=1000) :
        modelSetScaling(self.genreModel,size)

    def applyingIdfToGenreModel(self,size=1000) :
        for model in self.genreModel :
            for term in model[1] :
                term[1] = term[1] * self.idf[term[0]]

    def getGenreModelRank(self,rankSize) :
        genreModel_tmp = self.genreModel[:]
        ret = []
        for model in genreModel_tmp :
            sorted(model[1], key = lambda term : term[1],reverse=True)
            ret.append([model[0],model[1][0:rankSize]])
        return ret
    def showGenreModelRank(self,rankSize) :
        print("Print Genre Model Rank")
        ret = self.getGenreModelRank(rankSize)
        for genre in ret :
            print(genre[0])
            for term in genre[1] :
                print("%s : %10d\n" % (term[0],int(term[1])), end = '')
            print("")


# Model will be Scaled
def modelScaling(model,size) :
    total_tf = 0
    for term in model[1] :
        total_tf += term[1]
    for term in model[1] :
        term[1] = term[1] * 100/total_tf
def modelSetScaling(modelSet,size) :
    for model in modelSet :
        modelScaling(model,size)




class DeduceTarget :
    def __init__(self,path_testDataDir) :
        print("Heli")


class GenreDeducer :
    def __init__(self,path_trainDataDir,path_testDataDir,path_modelDataDir) :
        self.trainData = TrainData(path_trainDataDir)
        self.model = Model()
        self.deduceTarget = DeduceTarget(path_testDataDir)

    def doIndex(self) :
        self.trainData.indexScripts(self.trainData.path_trainDataDir)

    def doModeling(self,idf = False, scaling = False) :
        self.model.init(self.trainData)
        self.model.createFrame()
        self.model.createGenreModel(False)
        if idf :
            self.model.applyingIdfToGenreModel()
        if scaling :
            self.model.applyingScalingToGenreModel()

    def loadIndex(self,path_modelDataDir,num) :
        self.trainData.loadIndexData(path_modelDataDir,num)
    
    def showGenreModelRank(self,rankSize) :
        self.model.showGenreModelRank(rankSize)


genreDeducer = GenreDeducer("./data","./input","./model")
#genreDeducer.doIndex()
#genreDeducer.trainData.saveIndexData()
genreDeducer.loadIndex("./model",1)
genreDeducer.doModeling(True,True)

genreDeducer.showGenreModelRank(5)


print("Hi, My name is new.py")