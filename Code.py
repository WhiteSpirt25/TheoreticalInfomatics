from collections import Counter
from math import log

def NBTrain(X,Y):
    #clsses
    classes = Counter()
    clasList = [row[0] for row in X]
    classes.update(clasList)
    clasFreq = classes.most_common()
    for i in range(len(clasFreq)):
        clasFreq[i]=(clasFreq[i][0],float(clasFreq[i][1])/len(X))
    clasFreq = dict(clasFreq)

    #word frequency in classes
    wordProbs = {}
    for clas in Y:
        words = open(clas + '.txt',encoding="utf8")
        words = words.read().split('\n')
        wordLines = []
        for line in words:
            wordLines.append(line.split(' '))
        totalWords = sum(int(row[1]) for row in wordLines)
        wordProb = {}
        for line in wordLines:
            wordProb.update( [(line[0], float(line[1])/totalWords)] )
        wordProbs.update({clas:wordProb})
    return clasFreq,wordProbs

def NBTrainNew(X,Y):
    #clsses
    classes = Counter()
    clasList = [row[0] for row in X]
    classes.update(clasList)
    clasFreq = classes.most_common()
    for i in range(len(clasFreq)):
        clasFreq[i]=(clasFreq[i][0],float(clasFreq[i][1])/len(X))
    clasFreq = dict(clasFreq)

    #word frequency in classes
    wordProbs = {}
    for clas in Y:
        words = open(clas + 'New.txt',encoding="utf8")
        words = words.read().split('\n')
        wordLines = []
        for line in words:
            wordLines.append(line.split(' '))
        wordProb = {}
        for line in wordLines:
            wordProb.update( [(line[0], float(line[1]))] )
        wordProbs.update({clas:wordProb})
    return clasFreq,wordProbs

def classificator(text,clasFreq,wordProb,classes):
    #splitting
    temp = [text[0].split(),text[1].split()]
    bestClass = classes[0]
    bestScore = -999999999.
    for clas in classes:
        score = float(clasFreq[clas])
        for word in temp[0]:
            score -= 2*log(wordProb[clas].get(word,1))#так как слова в заголовке важнее чем в тексте
        for word in temp[1]:
            score -= log(wordProb[clas].get(word,1))
        if score>bestScore:
            bestClass = clas
            bestScore = score
    return bestClass

#parsing
file = open("news_train.txt",encoding="utf8")
file = file.read()
file = file.translate({ord(c): None for c in '1234567890.,-:!?"\'/«»„“();'})
lines = file.split('\n')
data = []
for i in range(len(lines)):
    data.append(lines[i].split('\t'))
del data[60000]
y = ['science', 'style', 'culture', 'life', 'economics', 'business', 'travel', 'forces', 'media', 'sport']
X = []
Y = []
for row in data:
    Y.append(row[0])
    X.append(row[1:])

    
# #count
# for clas in y:
#     wordCounter = Counter()
#     for i in range(len(data)):
#         if i%600 == 0:print(i/600,'%')
#         if data[i][0] == clas:
#             text = data[i][1].lower().split() + data[i][2].lower().split()
#             wordCounter.update(text)
#     wordList = wordCounter.most_common()
#     wordFile = open(clas+'.txt','w',encoding="utf8")
#     for i in range(len(wordList)-1):
#         wordFile.write(wordList[i][0] +' '+ str(wordList[i][1]) + '\n')
#     wordFile.write(wordList[len(wordList)-1][0] +' '+ str(wordList[len(wordList)-1][1]))

clsssifierParams = NBTrainNew(data,y)

print('Writing to output')
file = open("news_test.txt",encoding="utf8")
file = file.read()
file = file.translate({ord(c): None for c in '.,-:!?"\'/«»„“();'})
lines = file.split('\n')
data = []
for i in range(len(lines)):
    data.append(lines[i].split('\t'))
del data[15000]
ans = []
for inp in data:
    ans.append(classificator(inp,clsssifierParams[0],clsssifierParams[1],y))
ansFile = open('ans.txt', 'w', encoding="utf8")
for i in range(len(ans)-1):
    ansFile.write(ans[i] + '\n')
ansFile.write(ans[len(ans)-1])
