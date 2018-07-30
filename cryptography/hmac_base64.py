import base64
import hmac
import hashlib

with open('lorem.txt', 'rb') as f:
    body = f.read()

hash = hmac.new(
    b'secret-shared-key-goes-here',
    body,
    hashlib.sha1,
)

digest = hash.digest()
print(base64.encodestring(digest))

'''
The base64 encoded string ends in a newline, which frequently needs to be stripped off when
embedding the string in HTTP headers or other formatting-sensitive contexts.
$ python3 hmac_base64.py
b'MvqI7hYoulZYJevQA/srugy67cc=\n'
'''