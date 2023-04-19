
# first of all import the socket library
import socket  
import json   
import random
from EllipticCurve import EllipticCurve       

# next create a socket object
s = socket.socket()        
print ("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345               

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))        
print ("socket binded to %s" %(port))

# put the socket into listening mode
s.listen(5)             

# a forever loop until we interrupt it or
# an error occurs
while True:

    # Establish connection with client.
    c, addr = s.accept()    
    print ('Got connection from', addr )

    # receive data from the client and decoding to get the string.
    data = c.recv(1024).decode()

    # Convert JSON object to a dictionary
    received_data = json.loads(data)
    a = received_data["a"]
    b = received_data["b"]
    p = received_data["p"]
    generator_point = tuple(received_data["generator_point"])
    sender_public_key = tuple(received_data["public_key"])

    elliptic_curve = EllipticCurve(a, b, p)
    private_key = 4

    public_key = generator_point

    for i in range(private_key - 1):
        public_key = elliptic_curve.point_addition(public_key, generator_point)

    data = {
        "public_key": public_key
    }

    # Convert dictionary to JSON object
    json_object = json.dumps(data)

    # send data to the client
    c.send(json_object.encode())

    shared_key = sender_public_key

    for i in range(private_key - 1):
        shared_key = elliptic_curve.point_addition(shared_key, sender_public_key)

    print("Shared key: ", shared_key)

    # Close the connection with the client
    c.close()

    break