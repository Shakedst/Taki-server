import socket
import sys
import time
import json

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 50000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

time.sleep(1)
json_kwargs = {'default': lambda o: o.__dict__, 'sort_keys': True, 'indent': 4}

message = '1234'

try:
    # Send data
    print >>sys.stderr, 'sending "%s"' % message
    sock.send(message)
    time.sleep(1)

    data = sock.recv(1024)
    print >> sys.stderr, 'received "%s"' % data

    while True:
        time.sleep(3)
        play_turn = {'card': {'color': 'red', 'value': '8'}, 'order': ''}
        sock.send(json.dumps(play_turn, **json_kwargs))
        print "sent"
        data = sock.recv(1024)
        print >> sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
