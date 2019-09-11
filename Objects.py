class Card(object):
    def __init__(self, color, value):
        """
        Function that initials the card.
        """
        self.color = color
        self.value = value



    
class Pack(object):
    def __init__(self):
        self.pack = []
    
class Deck(Pack):
    def __init__(self):
        pass

    def create_deck(self):
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


        