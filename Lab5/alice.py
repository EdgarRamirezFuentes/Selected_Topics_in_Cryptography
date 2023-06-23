import socket
import os

# ECDH Libraries
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

# Key generation
private_key = ec.generate_private_key(ec.SECP384R1())

# Sharing public key
public_key = private_key.public_key()

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 80

# connect to the server on local computer
s.connect(('localhost', port))

# Send the public key to the server
s.sendall(public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
))

# receive public key from the server
pem_public_key = s.recv(1024)

# Convert PEM object to public key object
sender_public_key = serialization.load_pem_public_key(
    pem_public_key,
    backend=default_backend()
)

shared_key = private_key.exchange(ec.ECDH(), sender_public_key)

encryption_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'',
    backend=default_backend()
).derive(shared_key)

# Sending message encrypted with shared key using AES in GCM mode
message = b'Hello Bob!'
aad = b'authenticated but unencrypted data'
aesgcm = AESGCM(encryption_key)
nonce = os.urandom(12)
cyphertext = aesgcm.encrypt(nonce, message, aad)

# Send nonce, aad and cyphertext to Bob
s.sendall(nonce)
s.sendall(aad)
s.sendall(cyphertext)

# Receive nonce, aad and cyphertext from Bob
nonce = s.recv(1024)
aad = s.recv(1024)
cyphertext = s.recv(1024)

# Decrypt message
aesgcm = AESGCM(encryption_key)
message = aesgcm.decrypt(nonce, cyphertext, aad)
plaintext = message.decode('utf-8')

print('Bob says: ' + plaintext)

# close the connection
s.close()
