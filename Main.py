from collections import Counter
from math import log

class naive_bais:
    clasFreq = dict()
    wordProb = {}
    classes = []
    words = None

    def count(self):
        for clas in self.classes:
            wordCounter = Counter()
            for i in range(len(data)):
                if Y[i] == clas:
                    text = X[i].lower().split()
                    wordCounter.update(text)
            wordDict = dict(wordCounter)
        self.words = wordDict

    def fit(self,X, Y):
        # classes
        classes = Counter()
        classes.update(Y)
        self.classes = list(classes)
        clasFreq = classes.most_common()
        for i in range(len(clasFreq)):
            clasFreq[i] = (clasFreq[i][0], float(clasFreq[i][1]) / len(X))
        clasFreq = dict(clasFreq)


        self.count()

        # word frequency in classes
        wordProbs = {}
        for clas in Y:
            totalWords = len(list(self.words))
            wordProb = {}
            for word in self.words:
                wordProb.update([(word, self.words[word] / totalWords)])
            wordProbs.update({clas: wordProb})
        self.clasFreq = clasFreq
        self.wordProb = wordProb

    def predict1(self, text):
        # splitting
        temp = text.split()
        bestClass = self.classes[0]
        bestScore = -999999999.
        for clas in self.classes:
            score = -log(self.clasFreq[clas])
            for word in temp:
                score -= log(self.wordProb[clas].get(word, 1))
            if score > bestScore:
                bestClass = clas
                bestScore = score
        return bestClass

    def predict(self,arr):
        ans = []
        for text in arr:
            ans.append(self.predict1(text))
        return ans


# parsing
file = open("data", encoding="utf8")
file = file.read()
file = file.translate({ord(c): None for c in '1234567890.,-:!?"\'/«»„“();'})
lines = file.split('\n')
data = []
for i in range(len(lines)):
    data.append(lines[i].split('\t'))
data.pop()
X = []
Y = []
for row in data:
    Y.append(row[0])
    X.append(row[1])



from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = \
    train_test_split(X,Y,test_size=0.33)
clf = naive_bais()
clf.fit(x_train,y_train)
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test,clf.predict(x_test)))

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
