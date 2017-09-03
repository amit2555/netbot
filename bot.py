from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from lib.helpers import prefix, get_user
from netbot.operations.base import REGISTRY 
from preprocessor import Preprocessor 
import pandas as pd


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
               ('classifier', LinearSVC())
           ])

pipeline.fit(X, y)
print prefix('NetBot', 'How can I help you ' + USER + '?')

while not QUIT:
    utterance = raw_input(prefix(USER))
    if not utterance:
        continue
    if utterance in ('exit', 'quit', 'bye'):
        QUIT = True
        break 

    operation = REGISTRY[pipeline.predict([utterance])[0]]

    try:
        result, message = operation(utterance).run()
        print prefix('NetBot', message)
    except Exception, e:
        print prefix('NetBot', str(e))
        continue
