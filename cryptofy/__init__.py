import base64
import binascii
import getopt
import os
import sys

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

encoding = os.getenv('CRYPTOFY_ENCODING', 'utf-8')
secret_length = int(os.getenv('CRYPTOFY_SECRET_LENGTH', 16))


def decrypt(key, source, decode=True):
    """Decrypt string.

    Parameters
    ----------
    key : bytes
        The secret key.
    source : str or bytes
        The value to decrypt.
    decode : bool, optional
        Perform base64-decoding on `source` (default is True).

    Raises
    ------
    ValueError
        If the data padding is invalid.

    Returns
    -------
    bytes
        Decrypted value.
    """
    if decode:
        source = base64.b64decode(source.encode(encoding))

    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    iv = source[:AES.block_size]  # extract the iv from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, iv)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])

    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding.")

    return data[:-padding]  # remove the padding


def encrypt(key, source, encode=True):
    """Encrypt string.

    Parameters
    ----------
    key : bytes
        The secret key.
    source : bytes
        The value to encrypt.
    encode : bool, optional
        Return base64-encoded string (default is True).

    Returns
    -------
    str or bytes
        Encrypted value as base64-encoded string if `encode` is True, or as bytes object if `encode` is False.
    """
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    iv = Random.new().read(AES.block_size)  # generate iv
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding
    data = iv + encryptor.encrypt(source)  # store the iv at the beginning and encrypt

    return base64.b64encode(data).decode(encoding) if encode else data


def generate_secret(length=secret_length):
    """Generate random secret.

    Parameters
    ----------
    length : int
        The length of the returned secret.

    Returns
    -------
    bytes
        A random secret of size `length`.
    """
    return binascii.hexlify(os.urandom(length))


def main(argv):
    """Encrypt or decrypt from command line.

    Parameters
    ----------
    argv : list
        The arguments list
    """
    usage = 'usage: ' + __package__ + ' ((-d | -e) -k <key> -s <source>) | (-n [-l <length>])'

    try:
        options = 'hdek:l:ns:'
        long_options = [
            'help',
            'decrypt',
            'encrypt',
            'key=',
            'length=',
            'new-key',
            'source='
        ]

        opts, _ = getopt.getopt(argv, options, long_options)
    except getopt.GetoptError:
        print('Invalid syntax.\n' + usage, file=sys.stderr)
        sys.exit(2)

    cmd = ''
    key = ''
    length = ''
    new_key = False
    source = ''

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage)
            sys.exit()
        elif opt in ('-d', '--decrypt'):
            if cmd == '':
                cmd = 'decrypt'
            else:
                print('Option -d cannot be used together with -e.\n' + usage, file=sys.stderr)
                sys.exit(2)
        elif opt in ('-e', '--encrypt'):
            if cmd == '':
                cmd = 'encrypt'
            else:
                print('Option -e cannot be used together with -d.\n' + usage, file=sys.stderr)
                sys.exit(2)
        elif opt in ['-k', '--key']:
            key = arg
        elif opt in ('-l', '--length'):
            length = arg
        elif opt in ['-n', '--new-key']:
            new_key = True
        elif opt in ('-s', '--source'):
            source = arg

    if new_key:
        if cmd != '' or key != '' or source != '':
            print('Option -n can only be used with -l.\n' + usage, file=sys.stderr)
            sys.exit(2)

        if length == '':
            secret = generate_secret()
        else:
            secret = generate_secret(int(length))

        print(secret.decode(encoding))
    else:
        if cmd == '' or key == '' or source == '':
            print('Missing option(s).\n' + usage, file=sys.stderr)
            sys.exit(2)
        elif length != '':
            print('Option -l can only be used with -n.\n' + usage, file=sys.stderr)
            sys.exit(2)

        if cmd == 'decrypt':
            try:
                string = decrypt(bytes(key, encoding=encoding), source).decode(encoding)
            except ValueError as error:
                print(error, file=sys.stderr)
                sys.exit(2)
        else:
            string = encrypt(bytes(key, encoding=encoding), bytes(source, encoding))

        print(string)
