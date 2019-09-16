
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
        self.hands = dict((player, []) for player in self.players)
        self.deck = {}
        self.state = {
            'pile': None,
            'turn': None,
            'others': {},
            'hand': []
        }

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
        pass

        # 1. play the game with the given card and the given player_id.
        # 2. update the game state.
        # 3. change the self.state dict and keep it up to date.

        p_state = {
            'pile': None,
            'turn': self.get_next_player(),
            'others': {k: len(v) for k, v in self.hands.iteritems()}
        }

        self.state.update(p_state)





