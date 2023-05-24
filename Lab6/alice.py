import socket
import sys
import json
import base64

import utils

if __name__ == '__main__':
    # Key generation
    if not utils.generate_keys('alice'):
        print("Error generating keys!")
        sys.exit(1)

    s = socket.socket()
    port = 8080
    s.connect(('localhost', port))

    # Getting file to sign
    image_name = 'hacker.jpg'
    with open(f'./files/{image_name}', 'rb') as f:
        data = f.read()

        # Signing file
        signature = utils.sign_file('alice', data)  
        s.send(signature)
        s.send('alice'.encode('utf-8'))
        s.send(image_name.encode('utf-8'))

        f.close()
        

    s.close()



    
    