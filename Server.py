import select, socket, sys, Queue, time, json
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

game_is_started = False

new_users = []
normal_users = {}

json_kwargs = {'default': lambda o: o.__dict__, 'sort_keys': True, 'indent': 4}


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
                    # Either the client is new / registered => new_user / normal_user.
                    elif s in new_users:
                        # New Connections
                        if game_is_started:
                            message_queues[s].put('Game is undergoing')
                            continue

                        if THE_PASSWORD not in data:
                            message_queues[s].put('Wrong Password :(')
                            continue

                        new_users.remove(s)
                        normal_users[s] = Player(s)

                        message_queues[s].put('Login Successful')

                        if Player.p_count == 4:
                            game_is_started = True
                            for sock, p in normal_users.items():
                                message_queues[sock].put('Game Started, player ID ' + str(p.id))
                                new_state = json.dumps(game_manager.get_state(p.id), **json_kwargs)
                                message_queues[sock].put(new_state)

                    elif s in normal_users.keys():
                        # Normal communication
                        # try this for simple echo server: message_queues[s].put(data) # For simple Echo
                        print ("MSG FROM ", normal_users[s].id)
                        if game_is_started:
                            try:
                                # strip data to card and order
                                data = json.loads(data)
                                c_color = str(data['card']['color'])  # String
                                c_value = str(data['card']['value'])  # String
                                p_order = str(data['order'])  # String
                                answer = game_manager.update_game(normal_users[s].id, c_color, c_value, p_order)
                            except:
                                answer = 'Error[12]'

                            if answer != 'OK':
                                message_queues[s].put(json.dumps(answer))
                            else:
                                # This function will return a dictionary (Player: state)
                                # State includes:
                                #   -The current player's hand
                                #   -The other player's cards BY LENGTH
                                #   -Who's turn is the current turn
                                #   -What's the upper, faced up card of the pile
                                for sock, p in normal_users.items():
                                    new_state = game_manager.get_state(p.id)
                                    if new_state:
                                        message_queues[sock].put(json.dumps(new_state))
                        else:
                            message_queues[s].put("Error[11]")

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
