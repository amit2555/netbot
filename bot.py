from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from lib.helpers import prefix, get_user 
from netbot.operations.base import REGISTRY 
from preprocessor import Preprocessor 
import pandas as pd
import random


def identity(arg):
    return arg


USER = get_user()
QUIT = False

filepath = 'data/data.csv'
dataset = pd.read_csv(filepath, header=None, names=['message', 'label'])

X = dataset.message
y = dataset.label

pipeline = Pipeline([
               ('preprocessor', Preprocessor()),
               ('vectorizer', TfidfVectorizer(ngram_range=(1, 2), stop_words='english',
                                              lowercase=False, tokenizer=identity)),
               ('classifier', MultinomialNB())
           ])

pipeline.fit(X, y)

print prefix('How can I help you ' + USER + '?', 'NetBot')

while not QUIT:
    utterance = raw_input(USER + '> ')
    if not utterance:
        continue
    if utterance in ('exit', 'quit', 'bye'):
        QUIT = True
        print prefix(random.choice(['Goodbye', 'Bye']) , 'NetBot')
        break 

    operation = REGISTRY[pipeline.predict([utterance])[0]]
    
    result, message = operation(utterance).run()
    print result, message 
