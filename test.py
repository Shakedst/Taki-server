import socket
import sys
import time
import json
import random

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 50000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

time.sleep(1)
json_kwargs = {'default': lambda o: o.__dict__, 'sort_keys': True, 'indent': 4}

password = '1234'

try:
    # Send data
    # Connection setup
    print >>sys.stderr, 'sending Password "%s"' % password
    sock.send(password)

    data = sock.recv(1024)
    print >> sys.stderr, 'For Password "%s"' % data.strip()

    data = sock.recv(1024)
    print >> sys.stderr, 'For ID "%s"' % data.strip()

    # From now on each time
    time.sleep(1)
    while True:
        data = sock.recv(1024)
        print >> sys.stderr, 'For game state "%s"' % data.strip()

        if "Error[" not in data:
            los = json.loads(data.strip())
            hand = los['hand']
            print hand

        play_turn = {'card': hand[random.randint(0, len(hand) - 1)], 'order': ''}
        dus = json.dumps(play_turn, **json_kwargs)
        sock.send(dus)
        print dus
        print "sent"
        time.sleep(1)


finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
