class Card(object):
    def __init__(self, color, value):
        """
        Function that initializes the card.
        """
        self.color = color
        self.value = value

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
        from random import shuffle
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
        return self.pack.pop(-1) 
    
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


class Pile(Pack):
    """
    The center graveyard for cards.
    """
    def __init__(self):
        pass
    
    def show_top(self):
        """[Shows the "Upper" card of the deck]
        
        Returns:
            [Card] -- [Top of the pile]
        """
        return self.pack(-1)
    
    def receive_cards(self, cards):
        """
        Receives ne cards to the top of the pile
        
        Arguments:
            cards {Card / List of cards} -- The Card[s] we want to lay on the pile.
        """
        self.pack.add_cards(cards)




class Hand(Pack):
    """
    The few cards every player holds.
    """
    def __init__(self, deck, pile):
        self.deck = deck
        self.pile = pile
        self.draw_cards_from_deck(8)
    
    def draw_cards_from_deck(self, num_cards=1):
        """
        Draws cards from the deck into the hand.
        
        Keyword Arguments:
            num_cards {int} -- How many cards we want to draw (default: {1})
        """
        self.pack.add_cards(self.deck.provide_cards(num_cards))

