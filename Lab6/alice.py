import socket
import json

import utils

if __name__ == '__main__':
    #utils.generate_keys('alice')
    s = socket.socket()
    port = 80
    s.connect(('localhost', port))

    # Getting file to sign
    image_name = 'hacker.jpg'
    with open(f'./files/{image_name}', 'rb') as f:
        file_bytes = f.read()

        # Signing file
        signature = utils.sign_file('alice', file_bytes)  
        file_info = {
            'filename': image_name,
            'sender_name': 'alice',
        }

        s.sendall(signature)
        s.sendall(json.dumps(file_info).encode())
        
    s.close()
