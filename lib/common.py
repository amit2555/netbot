
def passed(message, *args):
    return ('PASS', message.format(*args))

def failed(message, *args):
    return ('FAIL', message.format(*args))
