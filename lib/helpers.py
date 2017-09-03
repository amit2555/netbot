from textwrap import dedent
import os


INDENT = 2


def prefix(user, text=' ', left_indent=True):
    return '\033[1m' + str(user) + '\033[0m' + '\n' + string_indent(text, left_indent)

def get_user():
    return os.getlogin().capitalize()

def string_indent(text, left_indent):
    return indent(str(text)) if left_indent else str(text)

def indent(text, ch=' '):
    padding = INDENT * ch
    return ''.join(padding+dedent(line.rstrip('\n')) for line in text.splitlines(True))
