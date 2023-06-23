import socket
import json

from utils import (
    verify_signature,
    generate_keys,
)

if __name__ == '__main__':
    s = socket.socket()
    port = 80
    s.bind(('', port))
    s.listen(5)

    while True:
        c, addr = s.accept()
        print('Got connection from', addr)

        # Receive file data
        signature = c.recv(1024)
        file_info = json.loads(c.recv(1024))

        filename = file_info['filename']
        sender_name = file_info['sender_name']

        with open(f'./files/{filename}', 'rb') as f:
            file_bytes = f.read()

            # Verify signature
            if verify_signature(sender_name, file_bytes, signature):
                print("Signature verified!")
            else:
                print("Signature verification failed!")

            # Fake verification
            if verify_signature('bob', file_bytes, signature):
                print("Signature verified!")
            else:
                print("Signature verification failed!")

            break

    s.close()