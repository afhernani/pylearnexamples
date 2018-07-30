# Compresion de datos y archivo python.'''Data Compression and Archiving python.'''

Aunque los sistemas informáticos modernos tienen una capacidad de almacenamiento cada vez mayor, el crecimiento en la cantidad de datos que se producen es implacable. Los algoritmos de compresión sin pérdida compensan parte del déficit en la capacidad por el tiempo invertido en la compresión o descompresión de datos para el espacio necesario para almacenarla. Python incluye interfaces con las bibliotecas de compresión más populares para que pueda leer y escribir archivos de forma intercambiable.
'''
Although modern computer systems have an ever-increasing storage capacity, the growth in the amount of data being produced is unrelenting. Lossless compression algorithms make up for some of the shortfall in capacity by trading time spent compressing or decompressing data for the space needed to store it. Python includes interfaces to the most popular compression libraries so it can read and write files interchangeably.
'''

zlib y gzip, y bz2 proporcionan acceso al formato bzip2 más reciente. Ambos formatos funcionan en flujos de datos, independientemente del formato de entrada, y proporcionan interfaces para leer y escribir archivos comprimidos de forma transparente. Use estos módulos para comprimir un único archivo o fuente de datos.
'''
zlib and gzip, and bz2 provides access to the more recent bzip2 format. Both formats work on streams of data, without regard to input format, and provide interfaces for reading and writing compressed files transparently. Use these modules for compressing a single file or data source.
'''

La biblioteca estándar también incluye módulos para administrar formatos de archivo, para combinar varios archivos en un único archivo que se puede administrar como una unidad. El archivo tar lee y escribe el formato de archivo de cinta Unix, un estándar antiguo que todavía se usa mucho hoy en día debido a su flexibilidad. zipfile funciona con archivos basados en el formato popularizado por el programa de PC PKZIP, originalmente utilizado bajo MS-DOS y Windows, pero ahora también se usa en otras plataformas debido a la simplicidad de su API y la fácil portabilidad del formato.
'''
The standard library also includes modules to manage archive formats, for combining several files into a single file that can be managed as a unit. tarfile reads and writes the Unix tape archive format—an old standard still widely used today because of its flexibility. zipfile works with archives based on the format popularized by the PC program PKZIP, originally used under MS-DOS and Windows, but now also used on other platforms because of the simplicity of its API and the easy portability of the format.
'''
# zlib: GNU zlib compresion '''zlib: GNU zlib compression'''
En la libreria zlib del proyecto GNU el modulo provee de interfaz con muchas funciones de compresion
## Trabajando con datos en memoria. '''Working with Data in Memory'''
La forma más sencilla de trabajar con zlib requiere mantener todos los datos comprimidos o descomprimidos en la memoria.
'''
The simplest way of working with zlib requires holding all of the data to be compressed or decompressed in memory.
'''
zlib_memory.py

'''
import zlib
import binascii
original_data = b'This is the original text.'
print('Original :', len(original_data), original_data)
compressed = zlib.compress(original_data)
print('Compressed :', len(compressed),
    binascii.hexlify(compressed))
decompressed = zlib.decompress(compressed)
print('Decompressed :', len(decompressed), decompressed)
'''
compress() y descompress() ambas funciones toman una secuencia de bytes como argumento y devuelven una secuencia de bytes.

El ejemplo anterior demuestra que la versión comprimida de pequeñas cantidades de datos puede ser más grande que la versión no comprimida. Si bien los resultados reales dependen de los datos de entrada, es interesante observar la sobrecarga de compresión para pequeños conjuntos de datos.
'''
The previous example demonstrates that the compressed version of small amounts of data can be larger than the uncompressed version. While the actual results depend on the input data, it is interesting to observe the compression overhead for small data sets.
'''
zlib_lengths.py
'''
import zlib
original_data = b'This is the original text.'
template = '{:>15} {:>15}'
print(template.format('len(data)', 'len(compressed)'))
print(template.format('-' * 15, '-' * 15))
for i in range(5):
    data = original_data * i
    compressed = zlib.compress(data)
    highlight = ' * ' if len(data) < len(compressed) else ''
    print(template.format(len(data), len(compressed)), highlight)
'''
$ python3 	zlib_lengths.py
len(data) 	len(compressed)
--------------- ---------------
	0 	8*
	26	 32*
	52 	35
	78 	35
	104 	36
The * characters in the output highlight the lines where the compressed data takes up
more memory than the uncompressed version.

zlib admite varios niveles de compresión diferentes, lo que permite un equilibrio entre el costo computacional y la cantidad de reducción de espacio. El nivel de compresión predeterminado, zlib.Z_DEFAULT_COMPRESSION, es -1 y corresponde a un valor codificado que representa un compromiso entre el rendimiento y el resultado de la compresión. Esto actualmente corresponde al nivel 6
'''
zlib supports several different compression levels, allowing a balance between computational cost and the amount of space reduction. The default compression level, zlib.Z_DEFAULT_COMPRESSION , is -1 and corresponds to a hard-coded value that represents a compromise between performance and compression outcome. This currently corresponds to level 6 
'''
zlib_compresslevel.py
'''
import zlib
input_data = b'Some repeated text.\n' * 1024
template = '{:>5} {:>5}'

print(template.format('Level', 'Size'))
print(template.format('-----', '----'))

for i in range(0, 10):
    data = zlib.compress(input_data, i)
    print(template.format(i, len(data)))
'''
Un nivel de 0 significa que no hay compresión en absoluto. Un nivel de 9 requiere la mayor cantidad de cálculos y produce la salida más pequeña. Como muestra este ejemplo, se puede lograr la misma reducción de tamaño con niveles de compresión múltiples para una entrada determinada.
'''
A level of 0 means no compression at all. A level of 9 requires the most computation and produces the smallest output. As this example shows, the same size reduction may be achieved with multiple compression levels for a given input.
'''

$ python3 zlib_compresslevel.py
Level 	Size
----- 	----
0 	20491
1 	172
2 	172
3 	172
4 	98
5 	98
6 	98
7 	98
8 	98
9 	98

## compresion y descompresion incremental '''Incremental compression and decompression'''

El enfoque en memoria tiene inconvenientes que lo hacen poco práctico para casos de uso del mundo real. Su principal inconveniente es que el sistema necesita suficiente memoria para mantener al mismo tiempo las versiones comprimidas y sin comprimir almacenadas en la memoria. La alternativa es usar los objetos Comprimir y Descomprimir para manipular los datos de forma incremental, de modo que el conjunto de datos completo no tenga que caber en la memoria.
'''
The in-memory approach has drawbacks that make it impractical for real-world use cases. Its major drawback is that the system needs enough memory to hold both the uncompressed and compressed versions resident in memory at the same time. The alternative is to use Compress and Decompress objects to manipulate data incrementally, so that the entire data set does not have to fit into memory.
'''
zlib_incremental.py
'''
import zlib
import binascii
compressor = zlib.compressobj(1)

with open('lorem.txt', 'rb') as input:
    while True:
        block = input.read(64)
        if not block:
            break
        compressed = compressor.compress(block)
        if compressed:
            print('Compressed: {}'.format(
                binascii.hexlify(compressed)))
        else:
            print('buffering...')
    remaining = compressor.flush()
    print('Flushed: {}'.format(binascii.hexlify(remaining)))

'''
Este ejemplo lee pequeños bloques de datos de un archivo de texto plano y pasa el conjunto de datos a compress (). El compresor mantiene un buffer interno de datos comprimidos. Como el algoritmo de compresión depende de las sumas de comprobación y de los tamaños de bloque mínimos, es posible que el compresor no esté listo para devolver los datos cada vez que recibe más datos. Si no tiene listo un bloque comprimido completo, devuelve una cadena de bytes vacía. Cuando se ingresan todos los datos, el método flush () fuerza al compresor a cerrar el bloque final y devolver el resto de los datos comprimidos.

'''
This example reads small blocks of data from a plain text file and passes the data set to compress() . The compressor maintains an internal buffer of compressed data. Since the compression algorithm depends on checksums and minimum block sizes, the compressor may not be ready to return data each time it receives more input. If it does not have an entire compressed block ready, it returns an empty byte string. When all of the data is fed in, the flush() method forces the compressor to close the final block and return the rest of the compressed data.
'''
$ python3 zlib_incremental.py
Compressed: b'7801'
buffering...
buffering...
buffering...
buffering...
buffering...
Flushed: b'55904b6ac4400c44f73e451da0f129b20c2110c85e696b8c40dde
dd167ce1f7915025a087daa9ef4be8c07e4f21c38962e834b800647435fd3b90
747b2810eb9c4bbcc13ac123bded6e4bef1c91ee40d3c6580e3ff52aad2e8cb2
eb6062dad74a89ca904cbb0f2545e0db4b1f2e01955b8c511cb2ac08967d228a
f1447c8ec72e40c4c714116e60cdef171bb6c0feaa255dff1c507c2c4439ec96
05b7e0ba9fc54bae39355cb89fd6ebe5841d673c7b7bc68a46f575a312eebd22
0d4b32441bdc1b36ebf0aedef3d57ea4b26dd986dd39af57dfb05d32279de'

## Mesclado de contenido de cadena. ''' Mixed Content Streams '''

La clase de descompresión devuelta por decompressobj () también se puede usar en situaciones donde los datos comprimidos y los datos no comprimidos se mezclan. '''The Decompress class returned by decompressobj() can also be used in situations where compressed data and uncompressed data are mixed together.'''

zlib_mixed.py
'''
import zlib
lorem = open('lorem.txt', 'rb').read()
compressed = zlib.compress(lorem)
combined = compressed + lorem
decompressor = zlib.decompressobj()
decompressed = decompressor.decompress(combined)
decompressed_matches = decompressed == lorem
print('Decompressed matches lorem:', decompressed_matches)
unused_matches = decompressor.unused_data == lorem
print('Unused data matches lorem :', unused_matches)
''''
Después de descomprimir todos los datos, el atributo de datos no utilizados contiene los datos no utilizados.'''After decompressing all of the data, the unused data attribute contains any data not used.'''

$ python3 zlib_mixed.py
Decompressed matches lorem: True
Unused data matches lorem : True

## Sumas de comprobación'''checksums'''
Además de las funciones de compresión y descompresión, zlib incluye dos funciones para calcular las sumas de comprobación de datos, adler32 () y crc32 (). Ninguna suma de comprobación es criptográficamente segura, y están destinadas a ser utilizadas solo para la verificación de integridad de datos.'''In addition to compression and decompression functions, zlib includes two functions for computing checksums of data, adler32() and crc32() . Neither checksum is cryptographically secure, and they are intended for use only for data integrity verification.'''
zlib_checksums.py
'''
import zlib
data = open('lorem.txt', 'rb').read()
cksum = zlib.adler32(data)
print('Adler32: {:12d}'.format(cksum))
print('       : {:12d}'.format(zlib.adler32(data, cksum)))
cksum = zlib.crc32(data)
print('CRC-32 : {:12d}'.format(cksum))
print('       : {:12d}'.format(zlib.crc32(data, cksum)))
'''
Ambas funciones toman los mismos argumentos: una cadena de bytes que contiene los datos y un valor opcional que se utilizará como punto de partida para la suma de comprobación. Devuelven un valor entero con signo de 32 bits que también puede transmitirse en llamadas posteriores como un nuevo argumento de punto de partida para producir una suma de comprobación en ejecución.'''Both functions take the same arguments: a byte string containing the data and an optional value to be used as a starting point for the checksum. They return a 32-bit signed integer value that can also be passed back on subsequent calls as a new starting-point argument to produce a running checksum.'''

$ python3 zlib_checksums.py
Adler32: 3542251998
       : 669447099
CRC-32 : 3038370516
       : 2870078631

## Compresion de datos de red.'''Compressing Network Data'''
El servidor de la lista siguiente utiliza el compresor de flujo para responder a las solicitudes que consisten en nombres de archivo al escribir una versión comprimida del archivo en el zócalo utilizado para comunicarse con el cliente.'''The server in the next listing uses the stream compressor to respond to requests consisting of filenames by writing a compressed version of the file to the socket used to communicate with the client.'''

zlib_server.py
'''
import zlib
import logging
import socketserver
import binascii

BLOCK_SIZE = 64

class ZlibRequestHandler(socketserver.BaseRequestHandler):
    logger = logging.getLogger('Server')
    def handle(self):
        compressor = zlib.compressobj(1)
        # Find out which file the client wants.
        filename = self.request.recv(1024).decode('utf-8')
        self.logger.debug('client asked for: %r', filename)
        # Send chunks of the file as they are compressed.
        with open(filename, 'rb') as input:
            while True:
                block = input.read(BLOCK_SIZE)
                if not block:
                    break
                self.logger.debug('RAW %r', block)
                compressed = compressor.compress(block)
                if compressed:
                    self.logger.debug(
                        'SENDING %r',
                        binascii.hexlify(compressed))
                    self.request.send(compressed)
                else:
                    self.logger.debug('BUFFERING')

         # Send any data being buffered by the compressor.
         remaining = compressor.flush()
         while remaining:
             to_send = remaining[:BLOCK_SIZE]
             remaining = remaining[BLOCK_SIZE:]
             self.logger.debug('FLUSHING %r',
                 binascii.hexlify(to_send))
             self.request.send(to_send)
         return


if __name__ == '__main__':
    import socket
    import threading
    from io import BytesIO
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(name)s: %(message)s',
    )
    logger = logging.getLogger('Client')

    # Set up a server, running in a separate thread.
    address = ('localhost', 0) # Let the kernel assign a port.
    server = socketserver.TCPServer(address, ZlibRequestHandler)
    ip, port = server.server_address # What port was assigned?
    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)
    t.start()

    # Connect to the server as a client.
    logger.info('Contacting server on %s:%s', ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # Ask for a file.
    requested_file = 'lorem.txt'
    logger.debug('sending filename: %r', requested_file)
    len_sent = s.send(requested_file.encode('utf-8'))

    # Receive a response.
    buffer = BytesIO()
    decompressor = zlib.decompressobj()
    while True:
        response = s.recv(BLOCK_SIZE)
        if not response:
            break
        logger.debug('READ %r', binascii.hexlify(response))

        # Include any unconsumed data when
        # feeding the decompressor.
        to_decompress = decompressor.unconsumed_tail + response
        while to_decompress:
            decompressed = decompressor.decompress(to_decompress)
            if decompressed:
                logger.debug('DECOMPRESSED %r', decompressed)
                buffer.write(decompressed)
                # Look for unconsumed data due to buffer overflow.
                to_decompress = decompressor.unconsumed_tail
            else:
                logger.debug('BUFFERING')
                to_decompress = None
    # Deal with data reamining inside the decompressor buffer.
    remainder = decompressor.flush()
    if remainder:
        logger.debug('FLUSHED %r', remainder)
        buffer.write(remainder)
    full_response = buffer.getvalue()
    lorem = open('lorem.txt', 'rb').read()
    logger.debug('response matches file contents: %s',
        full_response == lorem)
    # Clean up.
    s.close()
    server.socket.close()

'''

Esta lista incluye algunos fragmentos artificiales para ilustrar el comportamiento del almacenamiento en búfer que ocurre cuando pasar los datos a compress () o descompress () no da como resultado un bloque completo de salida comprimida o no comprimida.'''This listing includes some artificial chunking to illustrate the buffering behavior that happens when passing the data to compress() or decompress() does not result in a complete block of compressed or uncompressed output.'''
El cliente se conecta al socket y solicita un archivo. Luego se repite, recibiendo bloques de datos comprimidos. Dado que un bloque puede no contener siempre toda la información necesaria para descomprimirlo por completo, el resto de los datos recibidos anteriormente se combina con los nuevos datos y se pasa al descompresor. A medida que los datos se descomprimen, se anexan a un búfer, que se compara con el contenido del archivo al final del bucle de procesamiento.'''The client connects to the socket and requests a file. Then it loops, receiving blocks of compressed data. Since a block may not always contain all of the information needed to decompress it entirely, the remainder of any data received earlier is combined with the new data and passed to the decompressor. As the data is decompressed, it is appended to a buffer, which is compared against the file contents at the end of the processing loop.'''
Aviso'''Warning'''
Este servidor tiene implicaciones de seguridad obvias. No lo ejecute en un sistema en Internet abierto o en cualquier entorno donde la seguridad sea un problema.'''This server has obvious security implications. Do not run it on a system on the open Internet or in any environment where security might be an issue.'''

$ python3 zlib_server.py
Client: Contacting server on 127.0.0.1:53658
Client: sending filename: 'lorem.txt'
Server: client asked for: 'lorem.txt'
....
...

# gzip: Read and Write GNU zip Files
## Writing Comrpessed Files
## Reading Compressed Data
## Working with Streams

# bz2:bzip2 Compression
## One-Shot Operations in Memory
## Incremental Compression and Descompression
## Mixed-Content streams
## Writing Compressed Files
## Reading Compressed Files
## Reading and Writing Unicode Data
## Compressing Network Data

# tarfile: Tar Archive Access
## Testing Tar files
## Reading Metadata from an Archive
## Extracting files from an archive
## Creating new Archives
## Using alternative archive member names
## Writing Data from sources other than files
## Appending to Archives
## Working with compressed archives

# zipfile: Zip Archive Access
## Testing Zip files
## Reading Metadata from an Archive
## Extracting Archive Files from an Archive
## Creating new Archives
## Using Alternative Archive Member Names
## Writing Data From Sources Other than files
## writing with a zipInfo instance
## Appending to Files
## Python Zip Archives
## Limitations