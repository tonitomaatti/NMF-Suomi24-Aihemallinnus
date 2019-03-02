import csv
import numpy as np
import string
#from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

from stop_words import get_stop_words
stops = get_stop_words('finnish')

res = []

with open("terveys.csv", 'r', encoding='UTF-8', newline='') as csv_file:
	header = 0;
	reader = csv.reader(csv_file, delimiter=',')
	for row in reader:
		if header == 0:
			header += 1
			continue
		x = row[3].split()
		x = [''.join(c for c in s if c not in string.punctuation) for s in x]
		x = [s for s in x if s]
		res.append(x)

with open("matkailu.csv", 'r', encoding='UTF-8', newline='') as csv_file:
	header = 0;
	reader = csv.reader(csv_file, delimiter=',')
	for row in reader:
		if header == 0:
			header += 1
			continue
		x = row[3].split()
		x = [''.join(c for c in s if c not in string.punctuation) for s in x]
		x = [s for s in x if s]
		res.append(x)
		
# Talteen: res.append(row[3].split())
# for i in range(5):	
#	print(len(res[i]))
#	print(res[i])


for i in range(5):
	print(len(res[i]))

res2 = []

for row in res:
	temp = []
	for word in row:
		
		if word not in stops:
			temp.append(word)
	res2.append(temp)

# print("vertaillaan res ja res2")
# print("res pituus: ")
# print(len(res))
# print("res2 pituus: ")
# print(len(res2))

# print("testi teksti kummastakin:")
# print(res[5])
# print(res2[5])


def pretokens(doc):
	return doc
	
vectorizer = TfidfVectorizer(analyzer='word', tokenizer=pretokens, preprocessor=pretokens, max_df = 0.9, min_df=2)
X = vectorizer.fit_transform(res2)
print("X shape: ")
print(X.shape)


words = np.array(vectorizer.get_feature_names())


nmf = NMF(n_components=2, solver='mu')
W = nmf.fit_transform(X)
H = nmf.components_

for i, topic in enumerate(H):
	print("Topic {}: {}".format(i + 1, ",".join([str(x) for x in words[topic.argsort()[-10:]]])))