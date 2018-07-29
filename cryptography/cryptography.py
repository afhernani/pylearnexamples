
import hashlib, os

def hash_file_own(pathfile):
    '''
    Devuelve una cadena que representa el codigo Hash-SHA1 del archivo.
    pathfile -> complete path and name of file.
    si no existe el fichero devuelve None.
    '''   
    if not os.path.isfile(pathfile):
        return None
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(pathfile, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return(hasher.hexdigest())

print(hash_file_own('anotherfile.txt'))
print(hash_file_own('myfile.jpg'))
print(hash_file_own('myfile2.jpg'))
print(hash_file_own('myfile3.jpg'))