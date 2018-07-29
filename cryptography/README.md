

```python
import hashlib
print(hashlib.algorithms_available)
print(hashlib.algorithms_guaranteed) #openSSl
```

    {'SHA256', 'DSA-SHA', 'sha3_256', 'blake2b', 'SHA384', 'shake_256', 'sha384', 'whirlpool', 'sha512', 'sha256', 'SHA512', 'sha', 'dsaWithSHA', 'SHA224', 'sha1', 'DSA', 'shake_128', 'MD4', 'SHA1', 'sha224', 'sha3_512', 'md4', 'sha3_224', 'blake2s', 'sha3_384', 'md5', 'RIPEMD160', 'MD5', 'SHA', 'ecdsa-with-SHA1', 'ripemd160', 'dsaEncryption'}
    {'sha1', 'shake_256', 'sha3_224', 'blake2s', 'sha3_384', 'sha384', 'md5', 'sha3_256', 'sha512', 'shake_128', 'sha256', 'blake2b', 'sha224', 'sha3_512'}
    

## MD5


```python
import hashlib
mystring = input('Enter String to hash: ')
# Assumes the default UTF-8
hash_object = hashlib.md5(mystring.encode())
print(hash_object.hexdigest())
```

    Enter String to hash: Hellow World
    a774eab3b7c1a9088bc34a36a5392419
    

## SHA1


```python
import hashlib
hash_object = hashlib.sha1(b'Hello World')
hex_dig = hash_object.hexdigest()
print(hex_dig)
```

    0a4d55a8d778e5022fab701977c5d840bbc486d0
    

## SHA224


```python
import hashlib
hash_object = hashlib.sha224(b'Hello World')
hex_dig = hash_object.hexdigest()
print(hex_dig)
```

    c4890faffdb0105d991a461e668e276685401b02eab1ef4372795047
    

## SHA256


```python
import hashlib
hash_object = hashlib.sha256(b'Hello World')
hex_dig = hash_object.hexdigest()
print(hex_dig)
```

    a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e
    

## SHA384


```python
import hashlib
hash_object = hashlib.sha384(b'Hello World')
hex_dig = hash_object.hexdigest()
print(hex_dig)
```

    99514329186b2f6ae4a1329e7ee6c610a729636335174ac6b740f9028396fcc803d0e93863a7c3d90f86beee782f4f3f
    

## SHA512


```python
import hashlib
hash_object = hashlib.sha512(b'Hello World')
hex_dig = hash_object.hexdigest()
print(hex_dig)
```

    2c74fd17edafd80e8447b0d46741ee243b7eb74dd2149a0ab1b9246fb30382f27e853d8585719e0e67cbda0daa8f51671064615d645ae27acb15bfb1447f459b
    

## Usando algoritmos OpenSSL
### Supongamos que queremos utilizar un algoritmo suministrado por OpenSSL. Usando la función hashlib.algorithms_available, podemos encontra algoritmos adicionales, en nuestro caso usamos el 'DSA' que está disponible en nuestro computador. podemos untilizarlo con un metodo actualizado.



```python
import hashlib
hash_object = hashlib.new('DSA')
hash_object.update(b'Hello World')
print(hash_object.hexdigest())
```

    0a4d55a8d778e5022fab701977c5d840bbc486d0
    

## Clave hashing


```python
import uuid
import hashlib
 
def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
 
new_pass = input('Please enter a password: ')
hashed_password = hash_password(new_pass)
print('The string to store in the db is: ' + hashed_password)
old_pass = input('Now please enter the password again to check: ')
if check_password(hashed_password, old_pass):
    print('You entered the right password')
else:
    print('I am sorry but the password does not match')
```

    Please enter a password: smn14uqf
    The string to store in the db is: 8e8b1f25e0de8b0a98b5b800e4f8e03459cd38234dafd4793ac611b56ad24727:e75129740af84e21904b2d217d458bf6
    Now please enter the password again to check: smn14uqf
    You entered the right password
    

## Hash MD5 con ficheros


```python
import hashlib
 
hasher = hashlib.md5()
with open('myfile.jpg', 'rb') as afile:
    buf = afile.read()
    hasher.update(buf)
print(hasher.hexdigest())
```

    c0375e5b3e362362a8d69606bdd1a7a3
    


```python
hasher = hashlib.md5()
with open('myfile2.jpg', 'rb') as afile:
    buf = afile.read()
    hasher.update(buf)
print(hasher.hexdigest())
```

    c0375e5b3e362362a8d69606bdd1a7a3
    

El codigo de arriba, calcula con MD5 el hash del fichero. el fichero se abre en modo rb, por lo que obtenemos sus datos en binario. las funciones hash y por tanto la MD5 necesita recibir la string en bytes, de este modo nos aseguramos de esto.
La funcion open lee el fichero y lo almacena en memoria, esto es peligroso por el hecho que no sabemos el tamaño del fichero, una mejor version seria controlar la cantidad de bytes leidos del fichero como sigue:



```python
import hashlib
BLOCKSIZE = 65536
hasher = hashlib.md5()
with open('anotherfile.txt', 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(BLOCKSIZE)
print(hasher.hexdigest())
```

    b6d28fe02f45bcb16312a27a27db99cd
    

Si queremos utilizar este código con otro algoritmo de encriptacion solo hay que sustituir hashlib.md5() por ejemplo por hashlib.sha1(), etc..
## SHA1 con ficheros


```python
import hashlib
BLOCKSIZE = 65536
hasher = hashlib.sha1()
with open('anotherfile.txt', 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(BLOCKSIZE)
print(hasher.hexdigest())
```

    0d203806897016f4658c9e5c134ababdbc6a1286
    

## Encoding and Decoding cadenas.
convertir cadenas 8-bits en cadenas unicode y viceverza (python 3)


```python
s = 'flügel'
```


```python
s #devuelve el mismo resultado
```




    'flügel'




```python
nonlat = '字'
print(nonlat)
```

    字
    


```python
b'prefix in Python 3.x'
```




    b'prefix in Python 3.x'




```python
b'字'
```


      File "<ipython-input-26-02a4464714ac>", line 1
        b'字'
            ^
    SyntaxError: bytes can only contain ASCII literal characters.
    


## Converting Python strings to bytes, and bytes to strings
si queremos convertir nuestra variable de cadena nonlaat en un objeto byte, podemos usar el metodo constructor bytes, sin embargo solo usamos la cadena con un argumento, obtenemos este error.


```python
bytes(nonlat)
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-32-b891568b2365> in <module>()
    ----> 1 bytes(nonlat)
    

    TypeError: string argument without an encoding



```python
bytes(nonlat, 'utf-8')
```




    b'\xe5\xad\x97'



Ahora tenemos nuestro objeto bytes, codificado en utf-8 ... pero exactamente que significa esto?? quiere decir que el caracter contenido en nuestra variable nonlat fue convertido en una cadena de codigo que significa 'su cadena' en cadena utf-8, es decir fue codificado. esto quiere decir que si utilizamos el metodo encode(), en nonlat, obtendriamos el mismo resultado. veamos:


```python
nonlat.encode()
```




    b'\xe5\xad\x97'




```python
nonlat.encode('utf-16')
```




    b'\xff\xfeW['



Since we can encode strings to make bytes, we can also decode bytes to make strings—but when decoding a bytes object, we must know the correct codec to use to get the correct result. For example, if we try to use UTF-8 to decode a UTF-16-encoded version of nonlat above:


```python
b'\xff\xfeW['.decode('utf-8')
```


    ---------------------------------------------------------------------------

    UnicodeDecodeError                        Traceback (most recent call last)

    <ipython-input-37-2259f245aa7f> in <module>()
    ----> 1 b'\xff\xfeW['.decode('utf-8')
    

    UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte



```python
b'\xff\xfeW['.decode('utf-16')
```




    '字'



## Writing non-ASCII Data to Files in Python 3.x

Como nota final sobre las cadenas en Python 3.xy Python 2.x, debemos asegurarnos de recordar que el uso del método abierto para escribir en archivos en ambas ramas no permitirá cadenas Unicode (que contienen caracteres no ASCII) para ser escrito en archivos. Para hacer esto, las cadenas deben estar codificadas.

Esto no es gran cosa en Python 2.x, ya que una cadena solo será Unicode si lo haces así (usando el método Unicode o str.decode), pero en Python 3.x todas las cadenas son Unicode por defecto, así que si queremos escribir una cadena de este tipo, por ejemplo nonlat, para archivar, necesitaríamos usar str.encode y el modo wb (binario) para abrir para escribir la cadena en un archivo sin causar un error, como ese:


```python
with open('nonlat.txt', 'wb') as f:
    f.write(nonlat.encode())
```

Además, cuando lee un archivo con datos que no son ASCII, es importante usar el modo rb y decodificar los datos con el códec correcto, a menos, por supuesto, que no le importe tener una traducción "italiana" para su "español".
