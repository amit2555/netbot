from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from netbot.lib.common import DEVICE_REGEX
import re


REPLACE_PATTERNS = [
    (r'won\'t', 'will not'),
    (r'can\'t', 'cannot'),
    (r'i\'m', 'i am'),
    (r'ain\'t', 'is not'),
    (r'(\w+)\'ll', '\g<1> will'),
    (r'(\w+)n\'t', '\g<1> not'),
    (r'(\w+)\'ve', '\g<1> have'),
    (r'(\w+)\'s', '\g<1> is'),
    (r'(\w+)\'re', '\g<1> are'),
    (r'(\w+)\'d', '\g<1> would')
    ]


class RegexpReplacer(object):
    def __init__(self, patterns=REPLACE_PATTERNS):
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]

    def replace(self, text):
        for (pattern, repl) in self.patterns:
            s = re.sub(pattern, repl, text)
        return s


class Preprocessor(RegexpReplacer):
    def __init__(self):
        super(Preprocessor, self).__init__()

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [self.tokenize(doc) for doc in X]

    def tokenize(self, doc, lemmatize=True, **kwargs):
        self.tokens = word_tokenize(doc)
        self.tokens = [self.replace(token) for token in self.tokens if not self.device_match(token)]
        if lemmatize:
            return self.lemmatize(lemma=kwargs.get('lemma', WordNetLemmatizer()))
        return self.tokens

    def lemmatize(self, lemma):
        return [lemma.lemmatize(token, 'v') for token in self.tokens]

    def device_match(self, token):
        return re.search(DEVICE_REGEX, token) 
