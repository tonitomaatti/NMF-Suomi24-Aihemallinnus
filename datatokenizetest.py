import csv
import numpy as np
import string
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords 

data= fetch_20newsgroups(remove=('headers', 'footers', 'quotes')).data

res = []

for row in data:
	x = row.split()
	x = [''.join(c for c in s if c not in string.punctuation) for s in x]
	x = [s for s in x if s]
	res.append(x)
	
res2 = []

stops = set(stopwords.words('english')) 

for row in res:
	temp = []
	for word in row:
		
		if word not in stops:
			temp.append(word)
	res2.append(temp)

def pretokens(doc):
	return doc
	
vectorizer = TfidfVectorizer(max_features=2000, analyzer='word', tokenizer=pretokens, 
preprocessor=pretokens, min_df=10)

X = vectorizer.fit_transform(res2)
print("X shape: ")
print(X.shape)


idx_to_word = np.array(vectorizer.get_feature_names())

nmf = NMF(n_components=20, solver='mu')
W = nmf.fit_transform(X)
H = nmf.components_

for i, topic in enumerate(H):
	print("Topic {}: {}".format(i + 1, ",".join([str(x) for x in idx_to_word[topic.argsort()[-10:]]])))