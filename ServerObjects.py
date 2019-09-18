
class Player(object):
    _count = 0
    def __init__(self, socket):
        Player._count += 1
        self.id = Player._count
        self.socket = socket
