from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
import pandas as pd


dataset = 'data.csv'

dataset = pd.read_csv(dataset, header=None, names=['message', 'label'])
dataset['label_num'] = dataset.label.map({'LinkShutdown':0,
                                          'RestartProtocol':1})

messages = dataset.message
labels = dataset.label
vectorizer = TfidfVectorizer(ngram_range=(2, 3), stop_words='english')
X = vectorizer.fit_transform(messages)

clf = MultinomialNB()
#clf = SVC()
clf.fit(X, labels)
utterance  = ['do nothing']

features  = vectorizer.transform(utterance)
print(clf.predict(features)[0])

