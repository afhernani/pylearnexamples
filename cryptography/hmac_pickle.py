'''
Aplicación de firmas de mensajes.
HMAC authentication should be used for any public network service, and anytime data
is stored where security is important. For example, when sending data through a pipe or
socket, that data should be signed and then the signature should be tested before the data
is used. The extended example given here is available in the file hmac_pickle.py .
The first step is to establish a function to calculate a digest for a string, along with a
simple class to be instantiated and passed through a communication channel
'''
import hashlib
import hmac
import io
import pickle
import pprint

def make_digest(message):
    "Return a digest for the message."
    hash = hmac.new(
        b'secret-shared-key-goes-here',
        message,
        hashlib.sha1,
    )
    return hash.hexdigest().encode('utf-8')


class SimpleObject:
    """
    Demonstrate checking digests before unpickling.
    """
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name