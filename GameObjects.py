from random import shuffle, randint


class Card(object):
    def __init__(self, color, value):
        """
        Function that initializes the card.
        """
        self.color = color
        self.value = value

    def compare_cards(self, card):
        """
        Compares the card to a given card.
        
        Arguments:
            card {[Card]} -- Given card
        
        Returns:
            [tuple (Boolean, Boolean)] -- A tuple containing two boolean values which 
                                          describe the comparison of both cards' colors and values.
        """
        if card.color == 'ALL':
            return True, True
        
        return self.color == card.color, self.value == card.value

class Pack(object):
    def __init__(self):
        self.pack = []
    
    def add_cards(self, cards):
        """
        The function adds the given cards into the card list
        
        Arguments:
            cards {Card/List of Cards} -- the Card[s] we want to add to the pack.
        """
        self.pack.extend(cards)

    def remove_cards(self, num):
        """
        The function removes cards by a given amount.
        
        Arguments:
            num {[int]} -- [amount of cards to be removed]
        
        Returns:
            [list] -- [returns a list of the removed cards from the pack]
        """
        return [self.pack.pop() for _ in range(num)]
    
    def remove_random(self):
        """
        The function pops a random card from the pack.
        
        Returns:
            [Card] -- popped card
        """
        return self.pack.pop(randint(0,len(self.pack)-1))
    
    
class Deck(Pack):
    """
    The center Deck of the game.
    The one you draw cards from.
    """
    def __init__(self):
        self.create_deck()

    def create_deck(self):
        """
        [summary]
        The function initializes the deck with the cards
        according to Taki's specific rules.
        """
        colors = ['red', 'green', 'blue', 'yellow']
        numbers = range(1,10)
        signs = ['+', '+2', 'TAKI', 'CHDIR', 'STOP']
        special_cards = ['TAKI', 'CHCOL']
        for _ in range(2):
            for color in colors:
                for num in numbers:
                    self.pack.add_cards(Card(color, num))
                for sign in signs:
                    self.pack.add_cards(Card(color, sign))
            self.pack.add_cards(Card('ALL', value) for value in special_cards)
        self.pack = shuffle(self.pack)

    def pop_first(self):
        """[Pops the "Upper" card of the deck]
        
        Returns:
            card [Card] -- [Top of the deck]
        """
        return self.pack.pop() 
    
    def provide_cards(self, num_cards):
        """[Provides a specific amout of cards from the deck]
        
        Arguments:
            num_cards {[int]} -- [desired amount of cards to give]
        
        Returns:
            cards [list] -- [list of cards given]
        """
        cards = []
        for _ in range(num_cards):
            cards.append(self.pop_first())
        return cards
    
    def is_empty(self):
        """
        Tells if the Deck is empty
        
        Returns:
            [boolean] -- True - empty ; False - not empty
        """
        return not self.pack       


class Hand(Pack):
    """
    The few cards every player holds.
    """
    def __init__(self, deck):
        self.deck = deck
        self.draw_cards_from_deck(8)
    
    def draw_cards_from_deck(self, num_cards=1):
        """
        Draws cards from the deck into the hand.
        
        Keyword Arguments:
            num_cards {int} -- How many cards we want to draw (default: {1})
        """
        self.add_cards(self.deck.provide_cards(num_cards))

