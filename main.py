#-*- coding:utf-8 -*- 

# Team T2M
# S/S, 2019 Natural Language Processing & Information Retrival

# Project Subject : Movie Genre Classification by Script
# github link : https://github.com/jesn1219/nlp_t2m
#

from glob import *
import pickle
from Data_Preprocessing import *
import matplotlib.pyplot as plt
import numpy as np
import os
from excel_write import *
import math
from sklearn.metrics import hamming_loss

# return 
def test_getSimilarity(path_input) :
    indexed_inputSet = indexingTestFiles(path_input)
    queryModelSet = []
    for queryModel in indexed_inputSet :
        queryModelSet.append(make_and_scale_queryModel(queryModel, dataSource.modelFrame, dataSource))

    similarityResultSet = calGenreSimilarity(dataSource.modelSet, queryModelSet)
    return similarityResultSet

def test_getPrecision(similSet, rankRange) :
    precisionResult = [] 
    for sR  in similSet :
        name_tmp = sR[0]
        # [ '타이틀' '번위 이내 맞춘 빈도' '실제 장르' '정확도 예측 리스트' '맞춘 것만 리스트' ]
        precisionResult_unit = [sR[0], 0 , labeledGenre(name_tmp), sR[1][:], []  ] 
        #[ 'title', 잘 예측한 갯수, [랭킹값, 장르], 원래 장르 ]
        genreLabels_tmp = labeledGenre(name_tmp) 

        for rankIdx in range(rankRange) :
            genre_tmp = sR[1][rankIdx][0]
            if genre_tmp in  genreLabels_tmp :
                precisionResult_unit[4].append([rankIdx+1,genre_tmp])
                precisionResult_unit[1] += 1
        precisionResult.append(precisionResult_unit); 
    return precisionResult


# def testify(path_input) :
#     similSet = test_getSimilarity(path_input)
#
#     precision_of_testSet = test_getPrecision(similSet, 3)
#     testSize = len(precision_of_testSet)
#     precisionRate = 0
#     for i in precision_of_testSet :
#         print("%30s : %2d ; %s" %(i[0], i[1], i[2]))
#         precisionRate += i[1]
#     precisionRate = precisionRate /  testSize
#     print("Average Val : %f" % precisionRate)
#     print_and_save_result_to_excel(precision_of_testSet)
#     return precision_of_testSet
# testify all the scripts in input Folder

# @param [in]   datasource
# @param [in]   path to save result
def testify(path_input):
    simil_set = test_getSimilarity(path_input)
    genre_num = len(simil_set[0][1])
    true_labels = []
    pred_labels = []
    true_labels_01 = np.zeros((len(simil_set), genre_num), dtype='i')
    pred_labels_01 = np.zeros((len(simil_set), genre_num), dtype='i')
    label_names = []
    movie_names = []
    hl_results = []
    for s in simil_set[0][1]:
        label = s[0]
        label_names.append(label)
    for (i, simil) in zip(range(len(simil_set)), simil_set):
        name = simil[0]
        movie_names.append(name)
        pred_label = []
        true_label = labeledGenre(name)
        true_cnt = len(true_label)
        true_labels.append(true_label)
        pred_labels.append(pred_label)
        for c in range(1, true_cnt+1):
            pred_label.append(simil[1][-c][0])
        for true in true_label:
            true_labels_01[i][label_names.index(true)] = 1
        for pred in pred_label:
            pred_labels_01[i][label_names.index(pred)] = 1
        hl = hamming_loss(np.array(true_labels_01), np.array(pred_labels_01))
        hl_results.append(hl)
    hl_average = hamming_loss(np.array(true_labels_01), np.array(pred_labels_01))
    print_and_save_result_to_excel_hl(movie_names, true_labels, pred_labels, hl_results, hl_average)



# calGenreSimilarity(dataSource.modelSet, )
# Flag class
class Flags :
    def __init__(self) :
        self.exit_flag = False



# Class for Store data
class DataReposit :
    # indexed data : [ ['Genre', ['Title', [ 
    indexedSet = []
    modelFrame = []
    modelIdf = {}
    modelSet = []
    queryModel = []
     

    # Constructor
    def __init__(self) :
        print("Create DataReposit Object ")
    
    # indexing
    def indexing(self) :
        self.indexedSet = indexingScripts()
    
    # 벡터 공간을 만듬. 만들어진 벡터 공간 틀을 이용해 나중에 장르 벡터, 쿼리 벡터들을 만든다. 
    def create_modelFrame(self) :
        self.modelFrame = []
        for g in self.indexedSet :
            # indexedSet 안의 인덱싱 된 모델 g
            # g : ['Genre Name', [ (term, tf), (term2, tf), ........ ]]
            for t in g[1] :
                # t : (term, tf)
                if [t[0],0] in self.modelFrame :
                    # 이미 modelFrame에 해당 단어가 있다면 스킵
                    continue
                else :
                    # 틀에 단어 추가
                    self.modelFrame.append([t[0], 0])
    



    # 인덱스된 셋들을 가지고 장르 벡터 모델를 만든다. idf 딕셔너리도 만든다.
    def make_genreModel_and_idfDic(self) :
        for g in self.indexedSet :
            # g : 인덱싱 된 장르 모델
            # g : ['Genre Name', [ (term, tf), (term2, tf), ..... ]
            
            # 장르 벡터 모델을 초기화한다. modelFrame 사용
            tmpModel = [ g[0], self.modelFrame[:] ]
            for word in g[1] :
                # 인덱싱된 단어들 하나씩 장르 벡터 모델에 추가
                # word : ( term, tf )
                if [word[0],0] in tmpModel[1] :
                    tmpIdx = tmpModel[1].index([word[0],0])
                    tmpModel[1][tmpIdx] = [word[0], word[1]]

                    # idf 딕셔너리의 df 값 만들기
                    if word[0] in self.modelIdf.keys() :
                        self.modelIdf[word[0]] += 1
                    else :
                        self.modelIdf[word[0]] = 1
                    

            # 만들어진 장르 벡터 모델은 modelSet 리스트에 저장된다
            self.modelSet.append(tmpModel)
        # df 를 idf로 바꿈
        # idf setting
        for term in self.modelIdf :
            #print(self.modelIdf[term])
            self.modelIdf[term] = math.pow(1 + self.modelIdf[term],3)
            # idfval
            self.modelIdf[term] = 1 / self.modelIdf[term]
            
            #print(self.modelIdf[term])
        print("Hello")              




    # modelSet을 스케일링.
    def scale_ModelSet(self,size) :
        modelScaler(self.modelSet,size)
    
    def applying_idf_to_genreModel(self) :
        print("Before")
        for model in self.modelSet :
            model = applying_idf_to_model(self.modelIdf,model)
        print("After")

    # 장르 추측해내기.
    def predictGenre(self) :
        
        distances = []


        for g in self.modelSet :
            # 각 장르 벡터 모델 g 에 대해 계산
            distance = calModelDistance(g, self.queryModel[0]) # queryModel : [ ['title', [[term, tf], [term2, tf2]...] ] ]
            distances.append( [g[0], distance] )
        
        # distances 정렬
        ret = sorted(distances, key = lambda i : i[1], reverse = False)
        
        return ret

    # 시각화, 그래프 출력
    def showModel(self) :
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
        try :
            axQ = fig.add_subplot(6,5,tmp_idx)
            x = [i[0] for i in self.queryModel[0][1][:]]
            y = [i[1] for i in self.queryModel[0][1][:]]
            axQ.bar(x,y, width = 1.0, color = "red")
            axQ.set_title('Query : %s' % self.queryModel[0][0])
            #axQ.xaxis.set_major_formatter(plt.NullFormatter())
            #axQ.yaxis.set_major_locator(plt.NullLocator())
        except (IndexError) : 
            # 쿼리 벡터가 없을 때 except
            print('')

        plt.subplots_adjust(hspace = 1.0, wspace = 0.1)
        plt.show()




# @return [ ['title', [ [rank1, distance], [rank2, distance] ] , [ 'title2', [ [rank1, distance] ..... 
def calGenreSimilarity(genreModelset, queryModelset) :
    result = [] 
    for queryModel in queryModelset :
        distances = []
        # distances : [ [ 'genre1', distance ], [ 'genre2', distance] ... ]
        for genreModel in genreModelset :
            distance = calModelDistance(genreModel, queryModel)
            distances.append( [genreModel[0], distance] )
        result_unit = [queryModel[0],  sorted(distances, key = lambda i : i[1], reverse = False) ]
        # result_unit : [ 'title', [ [genre1, distance], [genre2, distance], ....(sorted list) 
        result.append(result_unit)
    return result

def loadInputFiles_and_makeQueryModel() :
    print("")



# 벡터 모델 스케일러
def modelScaler(modelSet,scale) :
    total_tf = 0
    for model in modelSet :
        total_tf = 0
        #Calculate total_tf
        for term in model[1] :
            total_tf += term[1]
        
        for term in model[1] :
            term[1] = term[1] * 100/total_tf
def applying_idf_to_model(idfDic, model) :
    retModel = model[:]
    for termData in retModel[1] :
        termData[1] = termData[1] * idfDic[termData[0]]
    return retModel

# 쿼리 날리기
# @param[in] modelFrame : use to make query vector
# @return   queryModel : vector model which was query
def querying(modelFrame, flags) :
    print("Input movie name to Classify Genre. ex) for Blade.txt :  >> Blade   ")
    print("If you want to see Graph, type >> show  ")
    print("To testify & save result to excel file, type >> testify")
    print("To terminate pregram, type >> exit")
    
    nameBuf = input()
    if nameBuf == 'show' :
        dataSource.showModel()
        return False
    if nameBuf == 'testify' :
        testify(path_testdir)
        return False
    if nameBuf == 'exit' :
        flags.exit_flag = True
        return False
    text = textFileImport(nameBuf)
    if text == '' :
        print("There is not %s.txt in ./input Directory" % nameBuf)
        return False
    
    print("Query Processing.. : %s " % nameBuf)
    indexedQuery = queryProcessing(text,nameBuf)
    queryModel = make_and_scale_queryModel(indexedQuery, modelFrame, dataSource)
    return queryModel



# 벡터 모델 유사도 계산
def calModelDistance(genreVector, queryVector) :
    # genre : [ 'title', [ [term,tf], [term, tf] .. ]]
    total_Distance = 0
    for idx in range(0, len(genreVector)) :
        total_Distance +=  np.square(genreVector[1][idx][1] - queryVector[1][idx][1])
    return total_Distance



# 쿼리로 들어온 스크립트 벡터모델로 만들기

# make_queryModel (indexedQuerySet, modelFrame) 
#

def make_and_scale_queryModel (indexedQuery, modelFrame, ds) :
    queryModelSet = []

    queryModel_tmp = [ indexedQuery[0], modelFrame[:]] 
    for word in indexedQuery[1] :
        if [ word[0],0 ] in queryModel_tmp[1] :
            tmpIdx = queryModel_tmp[1].index([word[0],0])
            queryModel_tmp[1][tmpIdx] = [word[0], word[1]]
        
        queryModelSet.append(queryModel_tmp) 
    modelScaler(queryModelSet, 1000)
    
    queryModel = queryModelSet[0]
    queryModel = applying_idf_to_model(ds.modelIdf , queryModelSet[0])
    return queryModel

# 삭제 예정, 위의 것으로 대체 
def make_model_to_query(indexedQuery, modelFrame) :
    
    tmpModel = [ indexedQuery[0], modelFrame[:] ]
    for word in indexedQuery[1] :
        # word : ( term, tf )
        if [word[0],0] in tmpModel[1] :
            tmpIdx = tmpModel[1].index([word[0],0])
            tmpModel[1][tmpIdx] = [word[0], word[1]]
    modelScaler([tmpModel],1000)


    return tmpModel


# input 폴더 안에서 name 파일을 찾아 읽고 반환 
def textFileImport(name) :
    if not (glob("./input/%s.txt" % name)) :
        return False
    else : 
        f = open("./input/%s.txt" % name, 'rt', encoding = 'utf-8')
        text = f.read()
        return text

# 영화 'name' 의 장르 반환 
def labeledGenre(name) :
    path_data = './data'
    genre_list = os.listdir(path_data)
    ret = []
    for gd in genre_list :
        if glob("./data/%s/%s.txt" % (gd, name)) :
            ret.append(gd)

    return ret





# makeNewModelData :
# True 이면, 장르 벡터 모델을 생성한다. 
# False이면, 계산하여 저장해 놓은 모델을 불러온다 indexedModel.t2m 으로 저장되어있음

makeNewModelData = False
dataSource = DataReposit()
path_testifyResult = "./"
path_data = "./data"
flags = Flags()

print("Hello")

if makeNewModelData :
    # 장르 벡터 모델 생성
    dataSource = DataReposit()
    dataSource.indexing()
    dataSource.create_modelFrame()
    dataSource.make_genreModel_and_idfDic()
    
    # 만든 장르 벡터 모델 저장 
    with open("savedModel.t2m", "wb") as file :
        pickle.dump(dataSource, file)
        print("Model Saved")
else :
    # 장르 벡터 모델 불러오기 
    with open("savedModel.t2m", "rb") as file :
        dataSource = pickle.load(file)
        dataSource.make_genreModel_and_idfDic()
# test
dataSource.create_modelFrame()

# 장르 벡터 모델 스케일링
dataSource.scale_ModelSet(1000)
dataSource.applying_idf_to_genreModel()


path_testdir = "./input"

# querying
while (True) :
    queryBuf = querying(dataSource.modelFrame, flags) 
    if flags.exit_flag == True :
        print("Terminate Program...")
        break
    if not queryBuf :
        continue
    else :
        dataSource.queryModel = [queryBuf]
        result = dataSource.predictGenre()
        
        rankIdx = 1
        for i in result :
            print("#%2d : %10s   Val : %6.2f" %(rankIdx, i[0], i[1] ))
            
            rankIdx +=1
             
        print("Actual Labeled Genre : ",  end = ' ')
        buf = labeledGenre(dataSource.queryModel[0][0]) 
        for w in buf  :
            print("%s  " % w, end = ' ' )
        print("")
        #dataSource.showModel(True)




































