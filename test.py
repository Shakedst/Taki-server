import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 50000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

time.sleep(1)

messages = [ '1234',
             'IM IN YAY',
             ]
amount_expected = len(''.join(messages))

try:

    # Send data
    for message in messages:
        print >>sys.stderr, 'sending "%s"' % message
        sock.sendall(message)
        time.sleep(1.5)

    # Look for the response
    amount_received = 0
    
    while True:
        data = sock.recv(1024)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data
        time.sleep(1.5)
        sock.send("Hi")

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()