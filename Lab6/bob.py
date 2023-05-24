import socket
import sys

from utils import (
    verify_signature,
    generate_keys,
)

if __name__ == '__main__':
    s = socket.socket()
    port = 8080
    s.bind(('', port))
    s.listen(5)

    # Generate keys
    if not generate_keys('bob'):
        print("Error generating keys!")
        sys.exit(1)

    while True:
        c, addr = s.accept()

        # Receive file data
        signature = c.recv(1024)
        username = c.recv(1024).decode('utf-8')
        image_name = c.recv(1024).decode('utf-8')

        with open(f'./files/{image_name}', 'rb') as f:
            data = f.read()

            # Verify signature
            if verify_signature(username, data, signature):
                print("Signature verified!")
            else:
                print("Signature verification failed!")

            # Fake verification
            if verify_signature('bob', data, signature):
                print("Signature verified!")
            else:
                print("Signature verification failed!")

            f.close()