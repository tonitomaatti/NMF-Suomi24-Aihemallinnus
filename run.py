#import csv
import numpy as np
import string
import json
import os

#from sklearn.datasets import fetch_20newsgroups

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.feature_extraction import text

import matplotlib.pyplot as plt

import re

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


lemmas = 3
text_sect = 13
text_sub = 14

inputFile = open("stopwords-fi.json", encoding='UTF-8')
finnishStops = json.load(inputFile, encoding='UTF-8')

moreStopWords = ["edes", "myös", "http", "www", "sä", "mä", "voida", "com", "esim", "/", "br" "," ".", "(", ")", "()", "()"]

customStops = text.ENGLISH_STOP_WORDS.union(finnishStops)
customStops = customStops.union(moreStopWords)

lemmaTexts = []
realTopics = []
textIDs = []

path = "./aineisto/"
for filename in os.listdir(path):
    with open(path + filename, 'r', encoding='UTF-8') as json_file:
        data = json.load(json_file)
        for row in data:
            if row.get("structs").get("text_id") in textIDs:
                continue
            textIDs.append(row.get("structs").get("text_id"))
            
            realTopics.append(row.get("structs").get("text_sub"))
            
            rawString = ""
            
            for token in row.get("tokens"):
                if token.get("lemma") is None:
                    continue
                    
                rawString += token.get("lemma")
                rawString += " "
            
            
                
            noHTMLString = cleanhtml(rawString)
            noURLString = re.sub(r'http\S+', '', noHTMLString)
            
            #if noURLString in lemmaTexts:, Testattu text_id:llä
            #    continue
            lemmaTexts.append(noURLString)

print("List of approved texts per topic: ")
for topic in set(realTopics):
        print(topic+": "+str(realTopics.count(topic)))

# , max_df = 0.9, min_df = 10
vectorizer = TfidfVectorizer(analyzer='word', stop_words = customStops, max_df = 0.9, min_df = 10)

numberOfTopics = len(set(realTopics))

X = vectorizer.fit_transform(lemmaTexts)


words = np.array(vectorizer.get_feature_names())

nmf = NMF(n_components=numberOfTopics, solver='mu')
W = nmf.fit_transform(X)
H = nmf.components_

for i, topic in enumerate(H):
    print("Aihe {}: {}".format(i + 1, ",".join([str(x) for x in words[topic.argsort()[::-1][:15]]])))

topicList = []

print("Mahdolliset keskustelualueet: ")
print(set(realTopics))

for i, topic in enumerate(H):
    givenTopic = input("Anna keskustelualue aiheelle " + str(i+1) + ": ")
    topicList.append(givenTopic)

predictedTopics = []

for array in W:
    topic = topicList[list(array).index(max(array))]
    predictedTopics.append(topic)

hit, miss = 0, 0

printedHits = 0
printedMisses = 0

for i, pTopic in enumerate(predictedTopics):
    if pTopic == realTopics[i]:
        if printedHits < 3:
            print("example of a hit: "+realTopics[i])
            print(lemmaTexts[i])
            print("---------------------")
            printedHits += 1
        hit += 1
    else:
        if printedMisses < 3:
            print("example of a miss: ")
            print("Real: " + realTopics[i]+", Predicted: "+pTopic )
            print(lemmaTexts[i])
            print("---------------------")
            printedMisses += 1
        miss += 1

print("Osumaprosentti:")
print(round(hit/(hit+miss), 2))

print("X shape: ")
print(X.shape)

print("W shape: ")
print(W.shape)

print("H shape: ")
print(H.shape)

varianceW = []
cutoff = 0
print("W array sums: ")
for array in W:
    varianceW.append(np.var(array))
    
#cutoff = int(round(len(predictedTopics))/100)
#[::-1][:cutoff] osa-arrayhyn

deltaIdxArray = np.array(varianceW).argsort()

sortedPredicted = []
sortedReal = []

for x in np.array(predictedTopics)[deltaIdxArray]:
    sortedPredicted.append(x)

for x in np.array(realTopics)[deltaIdxArray]:
    sortedReal.append(x)

eight = int(round(len(predictedTopics))/8)
eightCutOffs = [x*eight for x in [1,2,3,4,5,6,7,8]]

movingHitRate = []
hit, miss = 0, 0
eightRateArray = []
eightHit = 0
eightMiss = 0

for i in range(len(predictedTopics)):
    if i in eightCutOffs:
        print("eightRate: ")
        print(round(eightHit/(eightHit+eightMiss), 2))
        eightRateArray.append(round(eightHit/(eightHit+eightMiss), 2))
        eightHit = 0
        eightMiss = 0
    if sortedPredicted[i] == sortedReal[i]:
        eightHit += 1
        hit += 1
    else:
        eightMiss += 1
        miss += 1
    
    movingHitRate.append(round(hit/(hit+miss), 2))

plt.plot(movingHitRate)
plt.show()

plt.bar([1,2,3,4,5,6,7,8], eightRateArray, align='center')
plt.show()

# hit, miss = 0, 0
# for i in range (0, cutoff):
    # if sortedPredicted[i] == sortedReal[i]:
        # hit += 1
    # else:
        # miss += 1

# print("Osumaprosentti pruned:")
# print(round(hit/(hit+miss), 2))


