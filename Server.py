import select, socket, sys, Queue, time, pickle
from GameManagerClass import GameManagerSingleton
from ServerObjects import *

host_ip = raw_input("What is the host ip: ")
THE_PASSWORD = "1234"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind((host_ip, 50000))
server.listen(5)

print 'Server on address:', server.getsockname()[0]
print 'Listening on port:', server.getsockname()[1]

inputs = [server]
outputs = []
message_queues = {}

new_users = []
normal_users = {}


def on_disconnect(s, inputs, outputs, writable, message_queues):
    inputs.remove(s)
    if s in outputs:
        outputs.remove(s)

    if s in writable:
        writable.remove(s)

    if s in new_users:
        new_users.remove(s)
    
    if s in normal_users.keys():
        del normal_users[s]

    s.close()
    del message_queues[s]


try:
    game_manager = GameManagerSingleton()
    print "Setup complete"
    while inputs:
        # W8S here until a message has been received.
        readable, writable, exceptional = select.select(inputs, outputs, inputs, 0)

        for s in readable:
            if s is server:
                connection, client_address = s.accept()
                connection.setblocking(0)
                inputs.append(connection)
                outputs.append(connection)
                message_queues[connection] = Queue.Queue()
                print "Client Connected"
                new_users.append(connection)
            else:
                try:
                    data = s.recv(1024)
                except socket.error:
                    print "Client Disconnected"
                    on_disconnect(s, inputs, outputs, writable, message_queues)
                else:
                    if not data:
                        # The Client socket closed
                        print "Client Disconnected"
                        on_disconnect(s, inputs, outputs, writable, message_queues)

                    # So the client is online and we need to process the data
                    elif s in new_users:
                        # New Connections
                        if THE_PASSWORD in data:
                            new_users.remove(s)
                            normal_users[s] = Player(s)
                            # Send Game STATE
                            #message_queues[s].put(pickle.dumps(game_manager.game_state.export()))
                            message_queues[s].put('Login Successful')
                        else:
                            message_queues[s].put('Wrong Password :(')

                    elif s in normal_users.keys():
                        # Normal communication
                        message_queues[s].put(data) # For simple Echo
                        game_manager.update_game(normal_users[s], data)
                        # This function will return a dictionary (Player: state)
                        # State includes:
                        #   -The current player's hand
                        #   -The other player's cards BY LENGTH
                        #   -Who's turn is the current turn
                        #   -What's the upper, faced up card of the pile
                        for s, p in normal_users.items():
                            message_queues[s] = game_manager.get_state(p)
                        #turn = pickle.loads(data)

        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except Exception:
                pass
            else:
                s.send(next_msg)

        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]

except KeyboardInterrupt:
    print 'Interrupted Bye Bye'
    sys.exit(0)
