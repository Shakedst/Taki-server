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
    
class Deck(Pack):
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
                    self.pack.append(Card(color, num))
                for sign in signs:
                    self.pack.append(Card(color, sign))
            self.pack.append(Card('ALL', value) for value in special_cards)
        self.pack = shuffle(self.pack)

    def pop_first(self):
        """[Pops the "Upper" card of the deck. This function will remove the card from the pack]
        
        Returns:
            card [Card] -- [Top of the deck]
        """
        return self.pack.pop(0) 
    
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


        