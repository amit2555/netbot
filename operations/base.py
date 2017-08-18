from netbot.lib.common import extract_devices
from functools import partial
import re


REGISTRY = {}


class NoDevicesEntered(Exception):
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
            raise NoDevicesEntered

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
        return filter(fn, regex_list)

    @classmethod
    def sanitize_attributes(cls, user_attributes):
        if not user_attributes:
            return False
        sanitized_attributes = []
        for attribute in user_attributes:
            if len(attribute.split()) > 1:
                attr = re.sub(' ', '_', attribute)
                sanitized_attributes.append(attr)
            else:
                sanitized_attributes.append(attribute)
        return sanitized_attributes


def _regex_match(text, regex):
    match = re.search(regex, text)
    if match:
        return match.group(0)


def register(name):
    def wrapper(cls):
        REGISTRY[name] = cls
        return cls
    return wrapper 
