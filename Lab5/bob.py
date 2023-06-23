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

# Listen for incoming connections
s.bind(('', port))

# put the socket into listening mode
s.listen(5)

# a forever loop until we interrupt it or
# an error occurs
while True:
        # Establish connection with client.
        c, addr = s.accept()

        print('Got connection from', addr)

        # Receive public key from client
        pem_public_key = c.recv(1024)
    
        # Convert PEM object to public key object
        client_public_key = serialization.load_pem_public_key(
            pem_public_key,
            backend=default_backend()
        )


        # Respond to client with public key
        c.sendall(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
            
        shared_key = private_key.exchange(ec.ECDH(), client_public_key)

        # Using a Hash-based Key Derivation Function (HKDF) to derive a symmetric encryption key
        encryption_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'',
            backend=default_backend()
        ).derive(shared_key)
    
        # Receive nonce, aad and cyphertext from client
        nonce = c.recv(1024)
        aad = c.recv(1024)
        cyphertext = c.recv(1024)

        # Decrypt cyphertext using shared key using AES in GCM mode
        aesgcm = AESGCM(encryption_key)
        message = aesgcm.decrypt(nonce, cyphertext, aad)
        plaintext = message.decode('utf-8')
        
        print("Alice says: ", plaintext)

        # Reply to Alice
        reply_message = b'Hello Alice!'
        reply_nonce = os.urandom(12)
        reply_aad = b'Reply authenticated but unencrypted data'
        reply_aesgcm = AESGCM(encryption_key)
        reply_cyphertext = reply_aesgcm.encrypt(reply_nonce, reply_message, reply_aad)

        # Send nonce, aad and cyphertext to Alice
        c.sendall(reply_nonce)
        c.sendall(reply_aad)
        c.sendall(reply_cyphertext)

        break

# Close the connection with the client
c.close()
