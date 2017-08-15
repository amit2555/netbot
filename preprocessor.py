import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatize


replacement_patterns = [
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
    def __init__(self, patterns=replacement_patterns):
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]

    def replace(self, text):
        for (pattern, repl) in self.patterns:
            s = re.sub(pattern, repl, text)
        return s


class Preprocessor(RegexpReplacer):
    def __init__(self, utterance):
        super(Preprocessor, self).__init__()
        self.utterance = utterance

    def tokenize(self, lemmatize=True, **kwargs):
        self.tokens = word_tokenize(self.utterance)
        self.tokens = [self.replace(token) for token in self.tokens if token not in stopwords.words('english')]
        if lemmatize:
            return self.lemmatize(lemma=kwargs.get('lemma', WordNetLemmatize()))
        return self.tokens

    def lemmatize(self, lemma):
        return [lemma.lemmatize(token, 'v') for token in self.tokens]
