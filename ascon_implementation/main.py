from ascon import (
    ascon_encrypt, 
    ascon_decrypt,
    get_random_bytes
)

import base64
import os



def read_file_data(filename:str, directory:str) -> bytes:
    """Reads file data from a file in a directory.

    Args:
        filename (str): the name of the file to read
        directory (str): the directory to read the file from

    Returns:
        bytes: the data read from the file
    """
    with open(f'{directory}/{filename}', 'rb') as f:
        data = f.read()
    return data


def write_file_data(filename:str, directory:str, data:bytes) -> None:
    """Writes data to a file in a directory.
    
    Args:
        filename (str): the name of the file to write to
        directory (str): the directory to write the file to
        data (bytes): the data to write to the file
        
    Returns:
        None
    """
    with open(f'{directory}/{filename}', 'wb') as f:
        f.write(data)


def encryption(filename:str, key:bytes, nonce:bytes, associated_data:bytes, variant:str) -> None:
    """Does the encryption process (encrypt data and store encrypted data in a file).

    Args:
        filename (str): the name of the file to encrypt
        key (bytes): the key to use for encryption
        nonce (bytes): the nonce to use for encryption
        associated_data (bytes): the associated data to use for encryption
        variant (str): the variant of ascon ["Ascon-128", "Ascon-128a", "Ascon-80pq"] to use for encryption

    Returns:
        None
    """
    try: 
        directory = 'encrypted_data'
        source_directory = 'files'
        data = read_file_data(filename, source_directory)
        filename = filename.split('.')[0] + '.enc'

        ciphertext = ascon_encrypt(key, nonce, associated_data, data, variant)
        ciphertext = base64.b64encode(ciphertext)
        
        write_file_data(filename, directory, ciphertext)
    except Exception as e:
        print(e)
        # stop the program if an error occurs
        exit()

    
def decryption(filename:str, encrypted_data:bytes, key:bytes, nonce:bytes, associated_data:bytes, variant:str) -> None:
    """Does the decryption process (decrypt data and store decrypted data in a file).

    Args:
        filename (str): the name of the file to decrypt
        encrypted_data (bytes): the encrypted data to decrypt
        key (bytes): the key to use for decryption
        nonce (bytes): the nonce to use for decryption
        associated_data (bytes): the associated data to use for decryption
        variant (str): the variant of ascon ["Ascon-128", "Ascon-128a", "Ascon-80pq"] to use for decryption

    Returns:
        None
    """
    try:
        encrypted_data_directory = 'encrypted_data'
        encrypted_data_filename = filename.split('.')[0] + '.enc'
        directory = 'decrypted_data'

        encrypted_data = read_file_data(encrypted_data_filename, encrypted_data_directory)
        encrypted_data = base64.b64decode(encrypted_data)

        decrypted_data = ascon_decrypt(key, nonce, associated_data, encrypted_data, variant)

        write_file_data(filename, directory, decrypted_data)
    except Exception as e:
        print(e)
        # stop the program if an error occurs
        exit()

 
if __name__ == '__main__':

    ###################
    # ENCRYPTION DATA #
    ###################
    variant = 'Ascon-128a'
    key = get_random_bytes(20) if variant == "Ascon-80pq" else get_random_bytes(16)
    nonce = get_random_bytes(16)
    associated_data = b'Associated data'


    ##############
    # ENCRYPTION #
    ##############

    FILES = os.listdir('files')

    for filename in FILES:
        encryption(filename, key, nonce, associated_data, variant)

    ##############
    # DECRYPTION #
    ##############

    for filename in FILES:
        encrypted_filename = filename.split('.')[0] + '.enc'
        with open(f'encrypted_data/{encrypted_filename}', 'rb') as f:
            encrypted_data = base64.b64decode(f.read())

        decryption(filename, encrypted_data, key, nonce, associated_data, variant)

    print('Done!')
