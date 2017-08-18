import re


DEVICE_REGEX = re.compile(r'r\d+')


def passed(message, *args):
    return ('PASS', message.format(*args))

def failed(message, *args):
    return ('FAIL', message.format(*args))

def extract_devices(text):
    return re.findall(DEVICE_REGEX, text)
