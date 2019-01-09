y = ['science', 'style', 'culture', 'life', 'economics', 'business', 'travel', 'forces', 'media', 'sport']

#считываю и считаю вероятности слов
wordProbs = {}
for clas in y:
    words = open(clas + '.txt', encoding="utf8")
    words = words.read().split('\n')
    wordLines = []
    for line in words:
        wordLines.append(line.split(' '))
    totalWords = sum(int(row[1]) for row in wordLines)
    wordProb = {}
    for line in wordLines:
        wordProb.update([(line[0], float(line[1]) / totalWords)])
    wordProbs.update({clas: wordProb})

del clas
#чищу
for clas in y:
    wordProb = wordProbs[clas]
    newWords = dict()
    for word in wordProb:
        meanWordProb = 0
        for cls in y:
            if cls != clas:
                meanWordProb+=wordProbs[cls].get(word,0)
        meanWordProb /= len(y)-1
        if wordProb[word]>meanWordProb*1.3:
            newWords.update({word:wordProb[word]})
    file = open(clas + 'New.txt','w', encoding="utf8")
    for word in newWords:
        file.write(word + ' ' + str(wordProb[word]) + '\n')