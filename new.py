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
            pickle.dump(self,file)
            print("Index Data is Saved")

    def getIndexData(self) :
        return self.indexSet
class Model :
    def __init__(self,indexData) :
        self.indexData = indexData
    def createFrame(self) :
        self.frame = []
        for g in self.indexData :
            for t in g[1] :
                if [t[0],0] in self.frame :
                    continue
                else :
                    self.frame.append([t[0], 0])
    
    def createGenreModel(self,isScale) :
        self.genreModel = []
        print("Creating Genre Model")
        self.df = {}
        for g in self.indexData :
            tmpModel = [ g[0], self.frame[:] ]
            for word in g[1] :
                if [word[0],0] in tmpModel[1] : 
                    tmpIdx = tmpModel[1].index([word[0],0])
                    tmpModel[1][tmpIdx] = [word[0], word[1]]

                    if word[0] in self.idf.key() :
                        self.df[word[0]] += 1
                    else :
                        self.df[word[0]] = 1
            self.genreModel.append(tmpModel)
        print("Complete Creating Genre Model")

    def createIdf(self) :
        print("Creating idf Dictionary")
        self.idf = {}
        for term in self.df :
            self.idf[term] = math.log(1 + self.df[term],2)
            self.idf[term] = 1 / self.idf[term]
        print("Complete Creating idf Dictionary")
    
    def applyingScalingToGenreModel(self,modelSet,size) :
        modelSetScaling(modelSet,size)

    def applyingIdfToGenreModel(self,modelSet,size) :
        for model in modelSet :
            for term in model[1] :
                term[1] = term[1] * self.idf[term[0]]

    def getGenreModelRank(self,rankSize) :
        genreModel_tmp = self.genreModel[:]
        ret = []
        for model in genreModel_tmp :
            sorted(model[1], key = lambda term : term[1],reverse=True)
            ret.append([model[0],model[0:rankSize]])
        return ret
    def showGenreModelRank(self,rankSize) :
        print("Print Genre Model Rank")
        ret = self.getGenreModelRank(20)
        for genre in ret :
            print(genre[0])
            for term in genre :
                print("%s : %5d" % (term[0],term[1]), end = '')
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
        self.model = Model(path_modelDataDir)
        self.deduceTarget = DeduceTarget(path_testDataDir)

    def doIndex(self) :
        self.trainData.indexScripts(self.trainData.path_trainDataDir)

genreDeducer = GenreDeducer("./data","./input","./model")
genreDeducer.doIndex()
genreDeducer.trainData.saveIndexData()




print("Hi, My name is new.py")