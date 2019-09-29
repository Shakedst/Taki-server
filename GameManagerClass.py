from GameObjects import *

S_NOTHING, S_PLUS2, S_TAKI = range(3)


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
        self.hands = dict((player, self.deck.provide_cards(8)) for player in self.players)
        # Can be +2, and open Taki
        self.state = S_NOTHING
        self.plus2_counter = 0
        self.turn_dir = 1
        p_card = self.deck.remove_random()
        self.pile_color = p_card.color

        self.state = {
            'pile': p_card,  # the leading card
            'turn': self.players[0],  # the id of the player who play
            'turn_dir': self.turn_dir,
            'pile_color': self.pile_color,
            'others': {},  # the amount of cards each player holds by id
            'hand': []  # the current player hand
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
        cur_turn_index = self.players.index(self.state.get('turn'))
        return self.players[(cur_turn_index + 1) % len(self.players)]

    def update_game(self, player_id, card, order):
        """
        This function is being called every time we receive a message.
        Each time we get a message we have to check that the player_id is the one who has to play
        and then play the "game" for that move.

        1. play the game with the given card and the given player_id.
        2. update the game state.
        3. change the self.state dict and keep it up to date.

        :param player_id: int from 0 to players length
        :param card: value, color
        :param order: string stating to close taki or to draw a card or the chosen color for CHCOL
        :return: 'OK' if successful otherwise Error [##]
        """
        cur_turn = self.state.get('turn')
        if player_id != cur_turn:
            # Not your turn!
            return 'Error[01]'

        if order == 'draw card':
            if self.state == S_NOTHING:
                # Then take one card and move the turn forward
                pass
            elif self.state == S_PLUS2:
                # Then take two cards times the plus2_counter and move the turn forward
                pass
            elif self.state == S_TAKI:
                # take one and close the taki
                pass
            self.state = S_NOTHING

        elif card not in self.hands[player_id]:
            # Player has no such card!
            return 'Error[02]'

        if card.value == 'CHDIR':
            if card.color == self.pile_color:
                self.players.reverse()
                self.turn_dir *= -1
            else:
                # wrong color

        if card.value == 'STOP':


        # TODO
        # try  to put the card on the pile card
        # if you can continue else return the corresponding error

        # TODO
        # switch beteween the card of the pile to the current turn card and return the pile to the main deck
        # if needed change the turn to next one or leave it as it is if its a long turn (open taki => multiple cards).

        # For change direction just do: self.players.revers()

        p_state = {
            'pile': self.pile.get_pile_card(),
            'turn': self.get_next_player(),
            'others': {k: len(v) for k, v in self.hands.iteritems()}
        }

        self.state.update(p_state)
        return 'OK'
