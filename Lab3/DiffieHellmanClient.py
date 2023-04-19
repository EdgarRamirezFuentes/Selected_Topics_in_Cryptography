import socket            
import json 
import random
import math
from EllipticCurve import EllipticCurve

a = 2
b = 2
p = 17
elliptic_curve = EllipticCurve(a, b, p)
generator_point = (math.inf, math.inf)
private_key = 3

while generator_point == (math.inf, math.inf):
    generator_point = (5,1)

public_key = generator_point

for i in range(private_key - 1):
    public_key = elliptic_curve.point_addition(public_key, generator_point)

data = {
    "generator_point": generator_point,
    "a": a,
    "b": b,
    "p": p,
    "public_key": public_key
}

# Create a socket object
s = socket.socket()        

# Convert dictionary to JSON object
json_object = json.dumps(data)

# Define the port on which you want to connect
port = 12345             

# connect to the server on local computer
s.connect(('127.0.0.1', port))

# send data to the server
s.send(json_object.encode())
 
# receive data from the server and decoding to get the string.
sender_public_key = json.loads(s.recv(1024).decode())["public_key"]

shared_key = sender_public_key

for i in range(private_key - 1):
    shared_key = elliptic_curve.point_addition(shared_key, sender_public_key)

print("Shared key: ", shared_key)

# close the connection
s.close()    

     