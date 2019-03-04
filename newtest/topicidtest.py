import csv
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

moreStopWords = ["edes", "myös", "http", "www", "sä", "mä", "voida", "com", "esim", "/", "br" "," "."]

customStops = text.ENGLISH_STOP_WORDS.union(finnishStops)
customStops = customStops.union(moreStopWords)

lemmaStrings = []
realTopics = []

path = "./aineisto/"
for filename in os.listdir(path):
    with open(path + filename, 'r', encoding='UTF-8', newline='') as csv_file:
        header = 0;
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if header == 0:
                header += 1
                continue
            if not (row):
                continue
                
            noHTMLString = cleanhtml(row[lemmas])
            noURLString = re.sub(r'http\S+', '', noHTMLString)
            
            ##if noURLString in lemmaStrings:
            ##    continue
            lemmaStrings.append(noURLString)
            realTopics.append(row[text_sub])

vectorizer = TfidfVectorizer(analyzer='word', stop_words = customStops, max_df = 0.9, min_df = 10)

numberOfTopics = len(set(realTopics))

X = vectorizer.fit_transform(lemmaStrings)
print("X shape: ")
print(X.shape)

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

for i, pTopic in enumerate(predictedTopics):
    if pTopic == realTopics[i]:
        hit += 1
    else:
        miss += 1

print("Osumaprosentti:")
print(round(hit/(hit+miss), 2))



