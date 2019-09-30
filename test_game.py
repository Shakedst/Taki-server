from GameManagerClass import GameManagerSingleton
from GameObjects import *

game_manager = GameManagerSingleton()

player_id = 0
while True:
    c = raw_input('Enter card')
    color, value = ','.split(c)
    card = Card(color, value)
    order = raw_input('Enter order')
    game_manager.update_game(player_id,card,order)
