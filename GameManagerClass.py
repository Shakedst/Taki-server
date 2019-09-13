
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]
    
class GameManagerSingleton(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.hands = []
        self.deck = {}

    
    def get_state(self, player = None):
        pass
        return


    def update_game(self, client, card):
        pass
        return

