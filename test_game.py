from GameManagerClass import GameManagerSingleton
from GameObjects import *

game_manager = GameManagerSingleton()

def print_hand(hand):
    for i,c in enumerate(hand.pack):
        print i,c.color,c.value

player_id = 0
while True:
    print 'Player id:', player_id
    state = game_manager.get_state(player_id)
    print 'turn: ',state['turn'],', last card:',state['pile'].color,state['pile'].value,', others: ',state['others']
    print 'pile color: ',state['pile_color']
    my_hand = state['hand']
    print_hand(my_hand)
    index = int(raw_input('Enter card index: \n'))
    card = my_hand.pack[index]
    order = raw_input('Enter order: \n ').strip()
    answer = game_manager.update_game(player_id, card, order)
    print answer+'\n'
    if answer == 'OK':
        player_id = int(raw_input('Enter player id:\n'))

