import main
import pickle
from Data_Preprocessing import *
import matplotlib as plt
import numpy as np 
import os 
from excel_write import *
import math 
from glob import *





import Data_Preprocessing
class TrainData :
    def __init__(self, path_trainDataDir) :
        self.path_trainDataDir = path_trainDataDir

    def indexScripts(self,path_trainDataDir) :
        self.indexSet = Data_Preprocessing.indexingScripts(path_trainDataDir)
        
    def saveIndexData(self) :
        with open("indexData.t2m", "wb") as file :
            pickle.dump(self.indexSet,file)
            print("Index Data is Saved")
    def loadIndexData(self,path_indexDatasDir,num) :
        with open(path_indexDatasDir+"/indexData_"+str(num)+".t2m", "rb") as file :
            self.indexSet = pickle.load(file)
            print("Index Data is loaded")
    def getIndexData(self) :
        return self.indexSet
class GenreVectorModel :
    def __init__(self) :
        print("GVM Object Created")
        self.indexSet = []
    def createFrame(self) :
        self.frame = []
        for g in self.indexSet :
            for t in g[1] :
                if [t[0],0] in self.frame :
                    continue
                else :
                    self.frame.append([t[0], 0])
    
    def createGenreVector(self,isScale) :
        self.genreVectorModelSet = []
        print("Creating Genre Vector")
        self.df = {}
        for g in self.indexSet :
            tmpVector = [ g[0], self.frame[:] ]
            for word in g[1] :
                if [word[0],0] in tmpVector[1] : 
                    tmpIdx = tmpVector[1].index([word[0],0])
                    tmpVector[1][tmpIdx] = [word[0], word[1]]

                    if word[0] in self.df.keys() :
                        self.df[word[0]] += 1
                    else :
                        self.df[word[0]] = 1
            self.genreVectorModelSet.append(tmpVector)
        self.createIdf()
        print("Complete Creating Genre Vector")
    
    def init(self,indexData) :
        self.importIndexData(indexData)

    def importIndexData(self,indexData) :
        self.indexSet = indexData.getIndexData()

    def createIdf(self) :
        print("Creating idf Dictionary")
        #assert(self.genreVector == [])
        self.idf = {}
        numOfD = len(self.genreVectorModelSet)
        for term in self.df :
            # idf calculate
            self.idf[term] = math.log(1 + self.df[term],2)
            self.idf[term] = numOfD / self.idf[term]
        print("Complete Creating idf Dictionary")
    
    def doScalingToGenreVectorSet(self,size=1000) :
        vectorModelSetScaling(self.genreVectorModelSet,size)

    def applyingIdfToGenreVectorModelSet(self,size=1000) :
        for gvm in self.genreVectorModelSet :
            for term in gvm[1] :
                term[1] = term[1] * self.idf[term[0]]

    def getGenreVectorRank(self,rankSize) :
        genreVectors_tmp = self.genreVectorModelSet[:]
        ret = []
        for vector in genreVectors_tmp :
            vector[1] = sorted(vector[1], key = lambda term : term[1],reverse=True)
            ret.append([vector[0],vector[1][0:rankSize]])
        return ret
    def showGenreVectorRank(self,rankSize) :
        print("Print Genre Vector Rank")
        ret = self.getGenreVectorRank(rankSize)
        for genre in ret :
            print(genre[0])
            for term in genre[1] :
                print("%s : %10d\n" % (term[0],int(term[1])), end = '')
            print("")


# Vector will be Scaled
def vectorModelScaling(vector,size) :
    total_tf = 0
    for term in vector[1] :
        total_tf += term[1]
    for term in vector[1] :
        term[1] = term[1] * size/total_tf
def vectorModelSetScaling(vectorSet,size) :
    for vector in vectorSet :
        vectorModelScaling(vector,size)





class DeduceTarget :
    def __init__(self,path_testDataDir) :
        print("Heli")


class GenreDeducer :
    def __init__(self,path_trainDataDir,path_testDataDir,path_indexDatasDir) :
        self.trainData = TrainData(path_trainDataDir)
        self.genreVectorModel = GenreVectorModel()
        self.deduceTarget = DeduceTarget(path_testDataDir)
        self.path_indexDatasDir = path_indexDatasDir

    def doIndex(self) :
        self.trainData.indexScripts(self.trainData.path_trainDataDir)

    def doVectorModeling(self,idf = False, scaling = False, scalingSize = 1000) :
        self.genreVectorModel.init(self.trainData)
        self.genreVectorModel.createFrame()
        self.genreVectorModel.createGenreVector(False)
        if idf :
            self.genreVectorModel.applyingIdfToGenreVectorModelSet()
        if scaling :
            self.genreVectorModel.doScalingToGenreVectorSet(scalingSize)

    def loadIndex(self,indexData_num = 1) :
        self.trainData.loadIndexData(self.path_indexDatasDir,indexData_num)
    
    def showGenreVectorRank(self,rankSize) :
        self.genreVectorModel.showGenreVectorRank(rankSize)
    
    def initTestifySystem(self) :
        self.testifySystem = Testify(self.genreVectorModel, self.genreVectorModel.frame,self.genreVectorModel.idf)
    
    def initQuerySystem(self) :
        self.querySystem = QuerySystem(self.testifySystem)



class Testify :
    def __init__(self, GenreVectorModelObject, vectorFrame, idf,makeNewTestIndex = False, path_trainDataDir = "./trainData",path_indexDatasDir= "./indexDatas", path_testDataDir = "./testData") :
        print("He")
        self.path_trainDataDir = path_trainDataDir
        self.path_indexDatasDir = path_indexDatasDir
        self.path_testDataDir = path_testDataDir
        self.genreVectorModel = GenreVectorModelObject
        self.genreVectorModelSet = self.genreVectorModel.genreVectorModelSet
        if makeNewTestIndex == True :
            self.indexedTestDatas = indexingTestFiles(self.path_testDataDir)
            with open(self.path_indexDatasDir+"/indexData_test.t2m", "wb") as file :
                pickle.dump(self.indexedTestDatas,file)
                print("TestData Index file is saved")
        else :
            with open(self.path_indexDatasDir+"/indexData_test.t2m", "rb") as file :
                self.indexedTestDatas = pickle.load(file)
                print("TestData Index file is loaded ")

        self.idf = idf
        #self.createQueryVectorModelSet()
        self.testing()



    def getModelDistance(self,genreVectorModel, queryVectorModel) :
        #genere : ["title', [ [term,1], [term, tf] .. ]]
        distance = 0
        for index in range(0, len(genreVectorModel)) :
            distance += np.square(genreVectorModel[1][index][1] - queryVectorModel[1][index][1])
        return distance
        
    def getGenreSimilarityResults(self,genreVectorModelSet, queryVectorModelSet) :
        results = []
        for queryVectorModel in queryVectorModelSet :
            distances = []
            for genreVectorModel in genreVectorModelSet :
                distance = self.getModelDistance(genreVectorModel, queryVectorModel)
                distances.append( [genreVectorModel[0], distance])
            result_unit = [queryVectorModel[0], sorted(distances, key = lambda i : i[1], reverse = False)]
            results.append(result_unit)
        return results
    def createQueryVectorModelSet(self) :
        self.queryVectorModelSet = []
        for testQuery in self.indexedTestDatas[:] :
            processedQueryVectorModel = self.queryVectorModelProcessing(testQuery,self.genreVectorModel.frame, self.genreVectorModel.idf)
            self.queryVectorModelSet.append(processedQueryVectorModel)

    def queryVectorModelProcessing(self, indexedQuery, vectorFrame, idf) :
        queryVectorModel_tmp = [ indexedQuery[0], vectorFrame[:]]
        # Value copy
        for term in indexedQuery[1] :
            if [ term[0], 0] in queryVectorModel_tmp[1] :
                tmpIndex = queryVectorModel_tmp[1].index([term[0],0])
                queryVectorModel_tmp[1][tmpIndex] = [term[0], term[1]]        
        vectorModelScaling(queryVectorModel_tmp,10000)
        # Applying idf
        for term in queryVectorModel_tmp[1] :
            term[1] = term[1] * self.idf[term[0]]
        return queryVectorModel_tmp
    def testing(self) :
        # 테스트 파일들 인덱싱
        
        queryVectorModelSet = []
        # 테스트 파일 전처리
        for queryVectorModel in self.indexedTestDatas :
            queryVectorModelSet.append(self.queryVectorModelProcessing(queryVectorModel, self.genreVectorModel.frame, self.genreVectorModel.idf) )
        # 유사도 계산 후 저장
        resultSet = self.getGenreSimilarityResults(self.genreVectorModel.genreVectorModelSet, queryVectorModelSet)
        self.testingResult = resultSet
        return resultSet

    def getPrecision_R(self, rankRange) :
        precisionResult = []
        for sResult in self.testingResult :
            name_tmp = sResult[0]
            # labeledGenre 구형하기
            actualGenre = self.getLabeledGenre(name_tmp)
            precisionResult_unit = [sResult[0], 0, actualGenre, sResult[1][:], [] ]
            
            for rankIndex in range(rankRange) :
                genre_tmp = sResult[1][rankIndex][0]
                if genre_tmp in actualGenre :
                    precisionResult_unit[4].append([rankIndex+1, genre_tmp])
                    precisionResult_unit[1] += 1
            precisionResult.append(precisionResult_unit)
        return precisionResult


    def getLabeledGenre(self, name) :
        genre_list = os.listdir(self.path_trainDataDir)
        ret = []
        for gd in genre_list :
            if glob(self.path_trainDataDir+"/%s/%s.txt" % (gd, name)) :
                ret.append(gd)
        return ret




class QuerySystem :
    def __init__(self,TestifyObject) :
        print("QuerySystem Object craeted")
        self.testifySystem = TestifyObject
        self.finishFlag = False
        
    def run(self) :
        while(True) :
            queryBuf = self.querying(self.testifySystem.genreVectorModel.frame)
            if self.finishFlag == True :
                print("Terminate Querying")
                break
            if not queryBuf :
                continue
            else :
                print("Indiviual Query System")


    def querying(self, vectorFrame) :
        print("Input movie name to Classify Genre. ex) for Blade.txt :  >> Blade   ")
        print("If you want to see Graph, type >> show  ")
        print("To testify & save result to excel file, type >> testify")
        print("To terminate pregram, type >> exit")
        
        commandBuf = input()
        if commandBuf == 'testify' :
            print("Get Genre from TestDatas")
            print("R-precision")
            self.show_save_precision(3)
        elif commandBuf == 'exit' :
            self.finishFlag = True

        else :
            print("return QueryModel")
            
    def show_save_precision(self,rankSize) :
        testResult = self.testifySystem.getPrecision_R(rankSize)
        testDataSize = len(testResult)
        totalPrecisionRateSum = 0
        for i in testResult :
            print("%30s : %2d ; %s" %(i[0], i[1], i[2]))
            totalPrecisionRateSum += i[1]
        totalPrecisionRate = totalPrecisionRateSum/testDataSize
        print("Average Precision : %f" % totalPrecisionRate)
        print_and_save_result_to_excel(testResult)



genreDeducer = GenreDeducer("./trainData","./testCase","./indexDatas")
#genreDeducer.doIndex()
#genreDeducer.trainData.saveIndexData()
genreDeducer.loadIndex(1)
genreDeducer.doVectorModeling(idf=True,scaling=True,scalingSize=10000)

genreDeducer.initTestifySystem()
genreDeducer.initQuerySystem()
genreDeducer.querySystem.run()


genreDeducer.showGenreVectorRank(5)


print("Hi, My name is new.py")