from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from lib.helpers import prefix 
from netbot.operations.base import REGISTRY 
#from preprocessor import Preprocessor 
import pandas as pd
import os


USER = os.getlogin().capitalize()
QUIT = False

filepath = 'data/data.csv'
dataset = pd.read_csv(filepath, header=None, names=['message', 'label'])

messages = dataset.message
labels = dataset.label

vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
X = vectorizer.fit_transform(messages)

clf = MultinomialNB()
#clf = SVC()
clf.fit(X, labels)

print prefix('How can I help you ' + USER + '?', 'NetBot')

while not QUIT:
    utterance = raw_input(USER + '> ')
    features  = vectorizer.transform([utterance])
    operation = REGISTRY[clf.predict(features)[0]]
    
    result, message = operation(utterance).run()
    print result, message 
    print prefix('Goodbye.' , USER)
    QUIT = True
