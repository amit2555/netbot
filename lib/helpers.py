import os


def prefix(text, user):
    return user + '> ' + str(text)

def get_user():
    return os.getlogin().capitalize()
