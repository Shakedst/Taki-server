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
max_players = 4  # A number between 2 - 8

new_users = []
normal_users = {}

json_kwargs = {'default': lambda o: o.__dict__, 'sort_keys': True, 'indent': 1}

timeout_duration = 5  # secs
timeout_timer = timeout_duration


def serialize(msg):
    # Add a 4 byte length prefix to every message.
    len_prefix = len(msg.encode('utf-8'))
    return (str(len_prefix).zfill(4)) + msg


def on_disconnect(s, inputs, outputs, writable, message_queues):
    inputs.remove(s)

    if s in outputs:
        outputs.remove(s)

    if s in writable:
        writable.remove(s)

    if s in new_users:
        new_users.remove(s)

    if s in normal_users.keys():
        game_manager.client_disconnected(normal_users[s].id)
        del normal_users[s]

    del message_queues[s]
    s.close()


try:
    game_manager = GameManagerSingleton(max_players)
    print "Setup complete"
    while inputs:
        # W8S here until a message has been received.
        readable, writable, exceptional = select.select(inputs, outputs, inputs, 0)

        if game_is_started:
            if timeout_timer < time.time():
                print "True"
                curr_turn = game_manager.state.get('turn')
                # Forces the player to draw a card
                game_manager.update_game(curr_turn, "", "", "draw card")
                # Broadcast the new state to everyone
                for sock, p in normal_users.items():
                    # This function will return a dictionary (Player: State)
                    new_state = game_manager.get_state(p.id)
                    if new_state:
                        message_queues[sock].put(new_state)
                # Reset the timer
                timeout_timer = time.time() + timeout_duration

        if game_manager.game_is_finished or len(game_manager.players) == 0:
            print 'Game Over Bye Bye'
            print game_manager.state.get('winners')
            for s in outputs:
                s.send(serialize(json.dumps({'command': 'Game Over'}, **json_kwargs)))

            inputs = []
            server.close()

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
                    # Beware!
                    # TCP Protocol is a streaming protocol therefore if ONE client spams
                    # or sends a few messages too quickly the following line will take all the messages together
                    # and will NOT separate them which might cause problems trying to parse it or deserialize.
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
                            message_queues[s].put({'command': 'Game is undergoing'})
                            continue

                        if THE_PASSWORD not in data:
                            message_queues[s].put({'command': 'Wrong Password :('})
                            continue

                        new_users.remove(s)
                        normal_users[s] = Player(s)

                        message_queues[s].put({'command': 'Login Successful'})

                        if Player.p_count == game_manager.total_players:
                            game_is_started = True
                            timeout_timer = time.time() + timeout_duration
                            for sock, p in normal_users.items():
                                message_queues[sock].put({'command': 'Game Started, player ID ' + str(p.id)})
                                new_state = game_manager.get_state(p.id)
                                message_queues[sock].put(new_state)

                    elif s in normal_users.keys():
                        # Normal communication
                        # try this for simple echo server: message_queues[s].put(data) # For simple Echo
                        if game_is_started:
                            try:
                                # strip data to card and order
                                data = json.loads(data)
                                c_color = str(data['card']['color'])  # String
                                c_value = str(data['card']['value'])  # String
                                p_order = str(data['order'])  # String
                            except:
                                answer = {'error': '12'}
                            else:
                                answer = game_manager.update_game(normal_users[s].id, c_color, c_value, p_order)

                            # Empty string for error is OK therefore the turn was completed gracefully.
                            if answer['error'] != '':
                                message_queues[s].put(answer)
                            else:
                                for sock, p in normal_users.items():
                                    # This function will return a dictionary (Player: state)
                                    new_state = game_manager.get_state(p.id)
                                    if new_state:
                                        message_queues[sock].put(new_state)

                                timeout_timer = time.time() + timeout_duration
                        else:
                            message_queues[s].put({'error': '11'})

        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
                # Quick and dirty solution next_msg = str(next_msg) + ((1024 - len(next_msg.encode('utf-8'))) * ' ')
            except Queue.Empty:
                pass
            else:
                try:
                    s.send(serialize(json.dumps(next_msg, **json_kwargs)))
                except socket.error as e:
                    print 'Send Error' + str(e)

        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]

except KeyboardInterrupt:
    print 'Interrupted Bye Bye'
    sys.exit(0)


