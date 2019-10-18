import os

def tool():
    return os.environ['CFG_TOOL']

def mail():
    return os.environ['CFG_MAIL']

def key():
    return os.environ['CFG_KEY']
