from GameObjects import *

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]
    
class GameManagerSingleton(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.players = range(4)
        self.deck = Deck()
        self.hands = dict((player, None) for player in self.players)
        self.state = {
            'pile': self.deck.remove_random(),
            'turn': "",
            'others': {},
            'hand': []
        }


    def check_card_validation(self, player_id, card):
        cur_pile = self.state.get('pile')


        if player_id != self.state.get('turn'):
        # Not your turn!
            return 'Error[69]' 
        
        if card not in self.hands[player_id]:
        # Player has no such card!
            return 'Error[2]'
        
        if True not in cur_pile.compare_cards(card):
        # Color and Value not valid!
            return 'Error[3]'

            

        

        
        
        



    def get_state(self, player_id):
        # With a given player_id returns a dict with a game state
        if player_id is None:
            return ""

        return self.state.update(hand=self.hands[player_id])

    def get_next_player(self):
        # returns the next player from lower id number to higher or back to the lowest available
        # --! IMPORTANT !-- 
        # MUST check if the player is still in game ( available )
        pass

    def update_game(self, player_id, card):
        # This function is being called every time we receive a message.
        # Each time we get a message we have to check that the player_id is the one who has to play
        # and then play the "game" for that move.
        
        # 1. play the game with the given card and the given player_id.
        # 2. update the game state.
        # 3. change the self.state dict and keep it up to date.

        p_state = {
            'pile': self.state.get('pile'),
            'turn': self.get_next_player(),
            'others': {k: len(v) for k, v in self.hands.iteritems()}
        }

        
        self.state.update(p_state)





