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
        self.total_players = 4
        self.players = range(self.total_players)
        self.deck = Deck()
        self.hands = dict((player, Hand(self.deck)) for player in self.players)
        # Can be +2, and open Taki
        self.pile_state = S_NOTHING
        self.plus2_counter = 0
        p_card = self.deck.get_opening_card()
        self.colors = ['red', 'green', 'blue', 'yellow']

        self.state = {
            'pile': p_card,  # the leading card
            'turn': self.players[0],  # the id of the player who play
            'turn_dir': 1,  # the direction in which the turns go either up or down the IDs
            'pile_color': p_card.color,  # the color of the pile the same color as the pile card
            'others': {},  # the amount of cards each player holds by id
            'hand': [],  # the current player hand
            'winners': [None] * self.total_players  # list that the lower the index the higher the player position
        }

    def get_state(self, player_id):
        # With a given player_id returns a dict with a game state
        if player_id is None or player_id not in self.hands.keys():
            return ""

        self.state.update(hand=self.hands[player_id])
        return self.state

    def get_next_player(self):
        # returns the next player from lower id number to higher or back to the lowest available
        # --! IMPORTANT !-- 
        # MUST check if the player is still in game ( available )
        cur_turn_index = self.players.index(self.state.get('turn'))
        return self.players[(cur_turn_index + 1) % len(self.players)]

    def validate_card(self, card):
        return card.color == self.state.get('pile_color'), card.value == self.state.get('pile').value

    def update_winners(self):
        winners = self.state.get('winners')
        for player, hand in self.hands.iteritems():
            if not hand.pack:
                winners[winners.index(None)] = player
                if self.state.get('turn') == player:
                    self.state.update(turn=self.get_next_player())
                self.players.remove(player)

    def update_game(self, player_id, card_color, card_value, order):
        """
        This function is being called every time we receive a message.
        Each time we get a message we have to check that the player_id is the one who has to play
        and then play the "game" for that move.

        1. play the game with the given card and the given player_id.
        2. update the game state.
        3. change the self.state dict and keep it up to date.

        :param player_id: int from 0 to players length - 1
        :param card_color: A string stating the color
        :param card_value: A string stating the value
        :param order: a string that could be used as follows:
            close taki will come with last card of the taki
            draw a card will come with no card
            the chosen color for CHCOL card will the CHange COLor card
        :return: 'OK' if successful otherwise Error [##]
        """
        card = Card(card_color, card_value)

        cur_pile = self.state.get('pile')
        cur_turn = self.state.get('turn')

        # DEBUGGING
        print 'ID: ', player_id, 'card:', card, 'order:', order

        if player_id != cur_turn:
            # Not your turn!
            return 'Error[01]'

        if card_color == '' and card_value == '' and order == '':
            return 'Error[05]'

        if order == 'draw card':
            if self.pile_state == S_NOTHING:
                # Then take one card and move the turn forward
                self.hands[player_id].draw_cards_from_deck()    

            elif self.pile_state == S_PLUS2:
                # Then take two cards times the plus2_counter and move the turn forward
                self.hands[player_id].draw_cards_from_deck(num_cards=2 * self.plus2_counter)
                
            elif self.pile_state == S_TAKI:
                # take one and close the taki
                self.hands[player_id].draw_cards_from_deck()  
                 
            p_state = {
                'turn': self.get_next_player(),
                'others': {k: len(v.pack) for k, v in self.hands.iteritems()}
            }
        
            self.plus2_counter = 0
            self.state.update(p_state)
            self.pile_state = S_NOTHING
            return 'OK'

        trial_state = None
        if order == 'close taki':
            trial_state = S_NOTHING

        elif card not in self.hands[player_id].pack:
            # Player has no such card!
            return 'Error[02]'
        
        if True not in self.validate_card(card):
            # Color and Value not valid!
            return 'Error[03]'

        if self.pile_state == S_PLUS2:
            if card.value != '+2':
                return 'Error[03]'

        if card.value == 'CHDIR':
            self.state['turn_dir'] *= -1
            self.players.reverse()
            self.pile_state = S_NOTHING

        elif card.value == 'STOP':
            self.get_next_player()
            self.pile_state = S_NOTHING

        elif card.value == 'TAKI':
            self.pile_state = S_TAKI
                
        elif card.value == 'CHCOL':
            if order in self.colors:
                self.state['pile_color'] = order
                self.pile_state = S_NOTHING
            else:
                return 'Error[04]'
       
        elif card.value == '+2':
            self.pile_state = S_PLUS2
            self.plus2_counter += 1        

        if card.color != 'ALL':
            self.state['pile_color'] = card.color

        if trial_state is not None:
            self.pile_state = trial_state

        if self.pile_state != S_TAKI and card.value != '+':
            new_turn = self.get_next_player()
        else:
            new_turn = cur_turn

        self.hands[player_id].remove_card(card)
        self.deck.add_cards((cur_pile,))

        p_state = {
            'pile': card,
            'turn': new_turn,
            'others': {k: len(v.pack) for k, v in self.hands.iteritems()}
        }

        self.state.update(p_state)
        self.update_winners()
        return 'OK'
