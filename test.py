import socket
import sys
import time
import json
import random
import re

def choose_best_option(game):
    hand = game['hand']
    pile = game['pile']
    pile_color = game['pile_color']
    card_options = []

    for c in hand:
        if c['color'] == pile_color or c['value'] == pile['value']:
            card_options.append(c)

    if len(card_options) == 0:
        return None
    else:
        return card_options[0]
    
    return None


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

    data = sock.recv(1024)[4:]
    print >> sys.stderr, 'For Password "%s"' % data

    data = sock.recv(1024)[4:]
    my_id = int(re.findall('[0-9]', data)[0])
    print >> sys.stderr, 'For ID "%s"' % data[4:]
    
    # From now on each time
    time.sleep(1)
    while True:
        data = sock.recv(1024)[4:]
        print >> sys.stderr, 'For game state "%s"' % data

        if "Error[" not in data:
            game = json.loads(data)
            cur_turn = game['turn']

            if cur_turn == my_id: 
                card = choose_best_option(game)

                if card:
                    play_turn = {'card': card, 'order': ''}
                else:
                    play_turn = {'card': {"color": "", "value": ""}, 'order': 'draw card' }
                dus = json.dumps(play_turn, **json_kwargs)
                sock.send(dus)
        time.sleep(1)


finally:
    print >>sys.stderr, 'closing socket'
    sock.close()

