from testModel import *
from glob import *

class DataSource :
    dataset = []

        
    def __init__(self) :
        self.dataset = dataImport()


def textFileImport(genre) :
    scripts = []
    for textFile in glob("./data/%s/*.txt" % genre) :
        scripts.append(textFile)
    return scripts

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


dataSource = DataSource()

# Read and Index work loop
def wordIndex(fileInput) :
    print("START wordIndexing...")
    # Letter Token declare
    alphabet_low = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    alphabet_up = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    digits = ['1','2','3','4','5','6','7','8','9','10']
    sign = ['\'']

    # Token identifing function
    def isLetter(a) :
        if a in alphabet_low :
            return True
        elif a in alphabet_up :
            return True
        elif a in digits :
            return False
        elif a in sign :
            return True
        else :
            return False
    
    # open text file
    fi = fileInput
    
    # Declare carring text file variable
    if type(fi) == str :
        content = fi
    else : 
        content = fi.read()

    # This variable points letter index
    charIndex = 0

    # Word Buffer
    strBuf = ""

    # Letter Buffer
    charBuf = ""

    # Read and Index Work Flag
    readFlag = 1
    wordDic = {}

    # Operate and assign maximum index size to variable
    if type(fi) == str :
        MaxIndex = len(content)

    else :
        fi.seek(0,2)
        MaxIndex = fi.tell()-1

    # init letter index
    charIndex = -1

    try :
        while readFlag :
            charIndex += 1

            # check EOF
            if charIndex >= MaxIndex :
                break
        
            # Bring a next character
            charBuf = content[charIndex]

            # check character is valid : by using isLetter Function
            # At terminate of this loop, charIndex points first character of word.
        
            while not isLetter(charBuf):
                charIndex += 1
                # check EOF
                if charIndex >= MaxIndex :
                    readFlag = 0
                    break
                charBuf = content[charIndex]

            # check EOF
            if readFlag == 0 :
                break

            # Reading the word : starting at charIndex
            while (isLetter(charBuf)) :
                strBuf += charBuf
                charIndex += 1

                # check EOF
                if charIndex >= MaxIndex :
                    readFlag = 0
                    break
                charBuf = content[charIndex]
        
            # Word indexed as small letter
            # check the if word is in wordDic. and increase count of a word
            if strBuf.lower() in wordDic :
                wordDic[strBuf.lower()] += 1
            else :
                wordDic[strBuf.lower()] = 1
        
            # strBuf initilize
            strBuf = ""
    except IndexError :
        readFlag = 0    
    return wordDic

# Function for making VSM
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


index = []
for data in dataSource.dataset :
    
    textfiles = data[1]
    for textfile in textfiles :
        indexResult = wordIndex(open("%s" % textfile, 'r+', encoding='utf-8' ))
    index.append(indexResult)







''' 
# wordFilter create
ftmp = open("/Users/user/Desktop/anaconda/data/wordFilter.txt",'r')
wordFilter = wordIndex(ftmp)
# Reading Document Files
fileList = []
fileReading(fileList)
globalNumOfD = len(fileList)

# Indexing terms
documentsList = createTermsDic(fileList,wordFilter)

# Making VSM Model
VSMmodel = makeVSM(documentsList)

matA = np.array(VSMmodel).astype(np.float)

# Create SVD Matrices
U, s, Vt = np.linalg.svd( matA, full_matrices= True )

# Vt = np.transpose(V)

S = np.zeros((U.shape[1],Vt.shape[0]))
'''
'''
for i in range(0,len(s)) :
    S[i][i] = s[i]

for i in range(0,2) :
    S[i][i] = s[i]



testM = np.dot(U, np.dot(S,Vt))

print("origin matA")
print(matA.round(2))
print("testM")
print(testM.round(2))



print(s.round(2))

print("zeros print")
print(S.round(2))


X1 = np.dot(U,testM)
X2 = np.dot(testM,Vt)

termsX = []
termsY = []
for i in range(X2.shape[0]) :
    termsX.append(X2[i][0])
    termsY.append(X2[i][1])
    
for i in range(0, 500) :
    plt.scatter(termsX[i], termsY[i])
    plt.text(termsX[i], termsY[i], termsInfo[i], fontsize=9)
    


plt.show()

run()



#run(VSMmodels)
'''
