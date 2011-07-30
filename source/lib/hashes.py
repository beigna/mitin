
from hashlib import sha1
from uuid import uuid4


def salt():
    return sha1(uuid4().hex).hexdigest()

def encrypt(phrase, salt=''):
    print salt, phrase
    return sha1('%s%s' % (salt, phrase)).hexdigest()
