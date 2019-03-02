#selvitä miten saa toimimaan tfidf kirjastolla suoraan.
#IDEA: laita topic id feature_nameihin:

import csv
import numpy as np
import string
import json
import os

#from sklearn.datasets import fetch_20newsgroups

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.feature_extraction import text

#from stop_words import get_stop_words
#finnishStops = get_stop_words('finnish')

#text_sect = 7

inputFile = open("stopwords-fi.json", encoding='UTF-8')
finnishStops = json.load(inputFile, encoding='UTF-8')

moreStopWords = ["edes", "myös", "http", "www"]

customStops = text.ENGLISH_STOP_WORDS.union(finnishStops)
customStops = customStops.union(moreStopWords)

res = []
sections = []

path = "./aineisto/"
for filename in os.listdir(path):
    with open(path + filename, 'r', encoding='UTF-8', newline='') as csv_file:
        header = 0;
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if header == 0:
                header += 1
                continue
            res.append(row[3])
            sections.append(row[7])

##max_df = 0.9, min_df=2,
vectorizer = TfidfVectorizer(analyzer='word', stop_words = customStops)

X = vectorizer.fit_transform(res)
#print("X shape: ")
#print(X.shape)

words = np.array(vectorizer.get_feature_names())

nmf = NMF(n_components=2, solver='mu')
W = nmf.fit_transform(X)
H = nmf.components_

for i, topic in enumerate(H):
	print("Topic {}: {}".format(i + 1, ",".join([str(x) for x in words[topic.argsort()[-15:]]])))

print(sections)
input()