
## Zipfile: Acceso a archivo zip.'''Zip Archive Acces'''
El módulo zipfile se puede usar para leer y escribir archivos ZIP, el formato popularizado por el programa de PC PKZIP.'''The zipfile module can be used to read and write ZIP archive files, the format popularized by the PC program PKZIP.'''
### Prueba de archivos Zip.'''Testing Zip files.'''
La función is_zipfile () devuelve un valor booleano que indica si el nombre de archivo pasado como argumento se refiere a un archivo ZIP válido.'''The is_zipfile() function returns a boolean value indicating whether the filename passed as an argument refers to a valid ZIP archive.'''

zipfile_is_zipfile.py


```python
import zipfile
for filename in ['README.txt', 'example.zip',
    'bad_example.zip', 'notthere.zip']:
    print('{:>15} {}'.format(
        filename, zipfile.is_zipfile(filename)))

'''Si el archivo no existe, is_zipfile () devuelve False |
If the file does not exist at all, is_zipfile() returns False 
'''
'''$ python zipfile_is_zipfile.py'''
```

         README.txt False
        example.zip True
    bad_example.zip True
       notthere.zip True
    




    '$ python zipfile_is_zipfile.py'



## Lectura de metadatos de un archivo.'''Reading Metadata from an archive.'''
Use la clase ZipFile para trabajar directamente con un archivo ZIP. Esta clase admite métodos para leer datos sobre archivos existentes, así como para modificar los archivos al agregar más archivos.'''Use the ZipFile class to work directly with a ZIP archive. This class supports methods for reading data about existing archives as well as modifying the archives by adding more files.'''

zipfile_namelist.py


```python
import zipfile
with zipfile.ZipFile('example.zip', 'r') as zf:
    print(zf.namelist())
'''El método namelist() devuelve los nombres de los archivos en un archivo existente |
The namelist() method returns the names of the files in an existing archive'''
'''$ python zipfile_namelist.py'''
```

    ['aguila.jpg', 'JEFE-A ESTACION LZTE.pdf', 'Michael Page International 56-62 2011.zip']
    




    '$ python zipfile_namelist.py'



Sin embargo, la lista de nombres es solo parte de la información disponible del archivo. Para acceder a todos los metadatos sobre los contenidos ZIP, use los métodos infolist() y getinfo().'''The list of names is only part of the information available from the archive, though. To access all of the metadata about the ZIP contents, use the infolist() and getinfo() methods.'''

zipfile_infolist.py


```python
import datetime
import zipfile
def print_info(archive_name):
    with zipfile.ZipFile(archive_name) as zf:
        for info in zf.infolist():
            print(info.filename)
            print(' Comment :', info.comment)
            mod_date = datetime.datetime( * info.date_time)
            print(' Modified :', mod_date)
            if info.create_system == 0:
                system = 'Windows'
            elif info.create_system == 3:
                system = 'Unix'
            else:
                system = 'UNKNOWN'
            print(' System :', system)
            print(' ZIP version :', info.create_version)
            print(' Compressed :', info.compress_size, 'bytes')
            print(' Uncompressed:', info.file_size, 'bytes')
            print()
            
if __name__ == '__main__':
    print_info('example.zip')
```

    aguila.jpg
     Comment : b''
     Modified : 2011-07-15 12:46:22
     System : Windows
     ZIP version : 0
     Compressed : 2034 bytes
     Uncompressed: 2034 bytes
    
    JEFE-A ESTACION LZTE.pdf
     Comment : b''
     Modified : 2011-07-15 12:46:22
     System : Windows
     ZIP version : 0
     Compressed : 73495 bytes
     Uncompressed: 73495 bytes
    
    Michael Page International 56-62 2011.zip
     Comment : b''
     Modified : 2011-07-15 12:46:22
     System : Windows
     ZIP version : 0
     Compressed : 1235531 bytes
     Uncompressed: 1235531 bytes
    
    

Hay campos adicionales a los impresos aquí, pero descifrar los valores en algo útil requiere una lectura cuidadosa de la Nota de aplicación PKZIP con la especificación del archivo ZIP.'''There are additional fields other than those printed here, but deciphering the values into anything useful requires careful reading of the PKZIP Application Note with the ZIP file specification.'''

Si el nombre del miembro de archivo se conoce de antemano, su objeto ZipInfo se puede recuperar directamente con getinfo()'''If the name of the archive member is known in advance, its ZipInfo object can be retrieved directly with getinfo()'''

zipfile_getinfo.py


```python
import zipfile
with zipfile.ZipFile('example.zip') as zf:
    for filename in ['README.txt', 'notthere.txt']:
        try:
            info = zf.getinfo(filename)
        except KeyError:
            print('ERROR: Did not find {} in zip file'.format(
                filename))
        else:
            print('{} is {} bytes'.format(
                info.filename, info.file_size))
    '''Si el miembro de archivo no está presente, getinfo() genera un KeyError | 
    If the archive member is not present, getinfo() raises a KeyError '''
```

    ERROR: Did not find README.txt in zip file
    ERROR: Did not find notthere.txt in zip file
    

## Extrayendo archivos archivados del archivo.'''Extracting Archived Files From Archive.'''
Para acceder a los datos de un miembro de archivo, use el método read(), pasando el nombre del miembro.'''To access the data from an archive member, use the read() method, passing the member’s name.'''

zipfile_read.py


```python
import zipfile
with zipfile.ZipFile('example.zip') as zf:
    for filename in ['README.txt', 'notthere.txt']:
        try:
            data = zf.read(filename)
        except KeyError:
            print('ERROR: Did not find {} in zip file'.format(
                filename))
        else:
            print(filename, ':')
            print(data)
        print()
    '''Los datos se descomprimen automáticamente, si es necesario.|
    The data is automatically decompressed, if necessary.'''
```

    ERROR: Did not find README.txt in zip file
    
    ERROR: Did not find notthere.txt in zip file
    
    

## creando nuevos archivos.'''creating new archives.'''
Para crear un nuevo archivo, cree una instancia de ZipFile con un modo de 'w'. Cualquier archivo existente se trunca y se inicia un nuevo archivo. Para agregar archivos, use el método write().'''To create a new archive, instantiate the ZipFile with a mode of 'w' . Any existing file is truncated and a new archive is started. To add files, use the write() method.'''

zipfile_write.py


```python
from zipfile_infolist import print_info
import zipfile
print('creating archive')
with zipfile.ZipFile('write.zip', mode='w') as zf:
    print('adding README.txt')
    zf.write('README.txt')
print()
print_info('write.zip')
'''Por defecto, los contenidos del archivo comprimido no están comprimidos.|
By default, the contents of the archive are not compressed.'''
```

    creating archive
    adding README.txt
    
    README.txt
     Comment : b''
     Modified : 2018-07-31 02:46:30
     System : Windows
     ZIP version : 20
     Compressed : 310 bytes
     Uncompressed: 310 bytes
    
    




    'Por defecto, los contenidos del archivo comprimido no están comprimidos.|\nBy default, the contents of the archive are not compressed.'



Para agregar compresión, se requiere el módulo zlib. Si zlib está disponible, el modo de compresión para archivos individuales o para el archivo como un todo se puede establecer usando zipfile.ZIP_DEFLATED. El modo de compresión predeterminado es zipfile.ZIP_STORED, que agrega los datos de entrada al archivo sin comprimirlo.'''To add compression, the zlib module is required. If zlib is available, the compression mode for individual files or for the archive as a whole can be set using zipfile.ZIP_DEFLATED . The default compression mode is zipfile.ZIP_STORED , which adds the input data to the archive without compressing it.'''

zipfile_write_compression.py


```python
from zipfile_infolist import print_info
import zipfile
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED
modes = {
    zipfile.ZIP_DEFLATED: 'deflated',
    zipfile.ZIP_STORED: 'stored',
}
print('creating archive')

with zipfile.ZipFile('write_compression.zip', mode='w') as zf:
    mode_name = modes[compression]
    print('adding README.txt with compression mode', mode_name)
    zf.write('README.txt', compress_type=compression)
print()
print_info('write_compression.zip')

'''Esta vez, el miembro del archivo está comprimido. |
This time, the archive member is compressed.'''
```

    creating archive
    adding README.txt with compression mode deflated
    
    README.txt
     Comment : b''
     Modified : 2018-07-31 02:46:30
     System : Windows
     ZIP version : 20
     Compressed : 219 bytes
     Uncompressed: 310 bytes
    
    




    'Esta vez, el miembro del archivo está comprimido. |\nThis time, the archive member is compressed.'



## utilizando nombres de miembros de archivos alternativos.'''using alternative archive member names.'''

Pase un valor de arcname a write () para agregar un archivo a un archivo usando un nombre que no sea el original.'''Pass an arcname value to write() to add a file to an archive using a name other than the original filename.'''

zipfile_write_arcname.py


```python
from zipfile_infolist import print_info
import zipfile
with zipfile.ZipFile('write_arcname.zip', mode='w') as zf:
    zf.write('README.txt', arcname='NOT_README.txt')
print_info('write_arcname.zip')
'''
No hay ningún signo del nombre de archivo original en el archivo. |
There is no sign of the original filename in the archive.
'''
```

    NOT_README.txt
     Comment : b''
     Modified : 2018-07-31 02:46:30
     System : Windows
     ZIP version : 20
     Compressed : 310 bytes
     Uncompressed: 310 bytes
    
    




    '\nNo hay ningún signo del nombre de archivo original en el archivo. |\nThere is no sign of the original filename in the archive.\n'



## Escribir datos de fuentes que no sean archivos.'''Writing data from sources other than files.'''
A veces es necesario escribir en un archivo ZIP usando datos que no provienen de un archivo existente. En lugar de escribir los datos en un archivo y luego agregar ese archivo al archivo ZIP, use el método writestr () para agregar una cadena de bytes al archivo directamente.'''Sometimes it is necessary to write to a ZIP archive using data that did not come from an existing file. Rather than writing the data to a file and then adding that file to the ZIP archive, use the writestr() method to add a string of bytes to the archive'''

zipfile_writestr.py


```python
from zipfile_infolist import print_info
import zipfile
msg = 'This data did not exist in a file.'
with zipfile.ZipFile('writestr.zip',
                     mode='w',
                     compression=zipfile.ZIP_DEFLATED,
                    ) as zf:
    zf.writestr('from_string.txt', msg)
print_info('writestr.zip')
with zipfile.ZipFile('writestr.zip', 'r') as zf:
    print(zf.read('from_string.txt'))
    '''En este caso, el argumento compress_type de ZipFile se 
    utilizó para comprimir los datos, 
    ya que writestr() no toma un argumento para especificar la compresión. |
    In this case, the compress_type argument to ZipFile was used to compress 
    the data, since writestr() does not take an argument to 
    specify the compression.'''
```

    from_string.txt
     Comment : b''
     Modified : 2018-07-31 17:34:02
     System : Windows
     ZIP version : 20
     Compressed : 36 bytes
     Uncompressed: 34 bytes
    
    b'This data did not exist in a file.'
    

## Escribir con una instancia de archivo zip.'''Writing with a zipfile instance.'''

Normalmente, la fecha de modificación se calcula cuando un archivo o cadena se agrega al archivo. Se puede pasar una instancia de ZipInfo a writestr () para definir la fecha de modificación y otros metadatos.'''Normally, the modification date is computed when a file or string is added to the archive. A ZipInfo instance can be passed to writestr() to define the modification date and other metadata.'''

zipfile_writestr_zipinfo.py


```python
import time
import zipfile
from zipfile_infolist import print_info
msg = b'This data did not exist in a file.'
with zipfile.ZipFile('writestr_zipinfo.zip',
                     mode='w',
                    ) as zf:
    info = zipfile.ZipInfo('from_string.txt',
                           date_time=time.localtime(time.time()),
                          )
    info.compress_type = zipfile.ZIP_DEFLATED
    info.comment = b'Remarks go here'
    info.create_system = 0
    zf.writestr(info, msg)
print_info('writestr_zipinfo.zip')

```

    from_string.txt
     Comment : b'Remarks go here'
     Modified : 2018-07-31 17:41:22
     System : Windows
     ZIP version : 20
     Compressed : 36 bytes
     Uncompressed: 34 bytes
    
    

En este ejemplo, la hora modificada se establece en la hora actual, 
los datos se comprimen y se usa el valor falso para create_system. 
Un simple comentario también está asociado con el nuevo archivo. | 
In this example, the modified time is set to the current time, 
the data is compressed, and false value for create_system is used.
A simple comment is also associated with the new file.

## Agregar a los archivos. | Append to files.
Además de crear nuevos archivos, es posible adjuntar a un archivo existente o agregar un archivo al final de un archivo existente (como un archivo .exe para un archivo autoextraíble). Para abrir un archivo para agregarlo, use el modo 'a'.
| In addition to creating new archives, it is possible to append to an existing archive or add an archive at the end of an existing file (such as a .exe file for a self-extracting archive). To open a file to append to it, use mode 'a'.

zipfile_append.py


```python
from zipfile_infolist import print_info
import zipfile
print('creating archive')
with zipfile.ZipFile('append.zip', mode='w') as zf:
    zf.write('README.txt')
print()
print_info('append.zip')
print('appending to the archive')
with zipfile.ZipFile('append.zip', mode='a') as zf:
    zf.write('README.txt', arcname='README2.txt')
print()
print_info('append.zip')
```

    creating archive
    
    README.txt
     Comment : b''
     Modified : 2018-07-31 02:46:30
     System : Windows
     ZIP version : 20
     Compressed : 310 bytes
     Uncompressed: 310 bytes
    
    appending to the archive
    
    README.txt
     Comment : b''
     Modified : 2018-07-31 02:46:30
     System : Windows
     ZIP version : 20
     Compressed : 310 bytes
     Uncompressed: 310 bytes
    
    README2.txt
     Comment : b''
     Modified : 2018-07-31 02:46:30
     System : Windows
     ZIP version : 20
     Compressed : 310 bytes
     Uncompressed: 310 bytes
    
    

## Archivos Python zip '''Python zip archives'''
Python puede importar módulos desde archivos ZIP utilizando zipimport, si esos archivos aparecen en sys.path. La clase PyZipFile se puede utilizar para construir un módulo adecuado para su uso de esta manera. El método adicional writepy () le dice a PyZipFile que escanee un directorio en busca de archivos .py y agregue el archivo .pyo o .pyc correspondiente al archivo. Si no existe ningún formulario compilado, se crea y agrega un archivo .pyc.
'''Python can import modules from inside ZIP archives using zipimport, if those archives appear in sys.path . The PyZipFile class can be used to construct a module suitable for use in this way. The extra method writepy() tells PyZipFile to scan a directory for .py files and add the corresponding .pyo or .pyc file to the archive. If neither compiled form exists, a .pyc file is created and added.'''

zipfile_pyzipfile.py


```python
import sys
import zipfile
if __name__ == '__main__':
    with zipfile.PyZipFile('pyzipfile.zip', mode='w') as zf:
        zf.debug = 3
        print('Adding python files')
        zf.writepy('.')
    #print(zf.namelist)
    for name in zf.namelist():
        print(name)
    print()
    sys.path.insert(0, 'pyzipfile.zip')
    import zipfile_pyzipfile
    print('Imported from:', zipfile_pyzipfile.__file__)
```

    Adding python files
    Adding files from directory .
    Compiling .\zipfile_append.py
    Adding zipfile_append.pyc
    Compiling .\zipfile_getinfo.py
    Adding zipfile_getinfo.pyc
    Adding zipfile_infolist.pyc
    Compiling .\zipfile_is_zipfile.py
    Adding zipfile_is_zipfile.pyc
    Compiling .\zipfile_namelist.py
    Adding zipfile_namelist.pyc
    Adding zipfile_pyzipfile.pyc
    Compiling .\zipfile_read.py
    Adding zipfile_read.pyc
    Compiling .\zipfile_write.py
    Adding zipfile_write.pyc
    Compiling .\zipfile_writestr.py
    Adding zipfile_writestr.pyc
    Compiling .\zipfile_writestr_zipinfo.py
    Adding zipfile_writestr_zipinfo.pyc
    Compiling .\zipfile_write_arcname.py
    Adding zipfile_write_arcname.pyc
    Compiling .\zipfile_write_compression.py
    Adding zipfile_write_compression.pyc
    zipfile_append.pyc
    zipfile_getinfo.pyc
    zipfile_infolist.pyc
    zipfile_is_zipfile.pyc
    zipfile_namelist.pyc
    zipfile_pyzipfile.pyc
    zipfile_read.pyc
    zipfile_write.pyc
    zipfile_writestr.pyc
    zipfile_writestr_zipinfo.pyc
    zipfile_write_arcname.pyc
    zipfile_write_compression.pyc
    
    Imported from: D:\Usuarios\Hernani\Storage\Documentos\python\zipfiles\zipfile_pyzipfile.py
    

Con el atributo de depuración de PyZipFile establecido en 3, la depuración verbosa se habilita y la salida se produce cuando el programa compila cada archivo .py que encuentra.
'''With the debug attribute of the PyZipFile set to 3 , verbose debugging is enabled and output is produced as the program compiles each .py file it finds.'''

## Limitaciones '''Limitations'''
El módulo zipfile no es compatible con archivos ZIP con comentarios adjuntos o archivos de discos múltiples. Admite archivos ZIP de más de 4 GB que utilizan las extensiones ZIP64.
'''The zipfile module does not support ZIP files with appended comments, or multi-disk archives. It does support ZIP files larger than 4 GB that use the ZIP64 extensions.'''
