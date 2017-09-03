from netbot.lib.common import passed, failed, extract_devices
from functools import partial
import string
import re


REGISTRY = {}
STRING_TABLE = string.maketrans("", "")


class NoDevicesFound(Exception):
    def __init__(self):
        Exception.__init__(self, 'User did not enter any device')


class NotImplemented(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class BaseOperation(object):
    REGEX = None

    def __init__(self, utterance):
        self.utterance = utterance
        self.devices = extract_devices(self.utterance) 
        if not self.devices_found:
            raise NoDevicesFound

        self.attributes = self.extract_attributes(self.utterance)

    def run(self, *args, **kwargs):
        raise NotImplemented('run method is not implemented')

    @property
    def devices_found(self):
        return False if not self.devices else True

    @classmethod
    def extract_attributes(cls, utterance):
        regex_list = getattr(cls, 'REGEX')
        if not regex_list:
            return False
        fn = partial(_regex_match, utterance)
        return [re.sub('[- ]', '_', attr.translate(STRING_TABLE, string.punctuation)) for attr in filter(fn, regex_list)]


def _regex_match(text, regex):
    match = re.search(regex, text)
    if match:
        return regex 


def register(name):
    def wrapper(cls):
        REGISTRY[name] = cls
        return cls
    return wrapper 
