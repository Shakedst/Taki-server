
class Player(object):
    id_list = []
    p_count = 0

    def __init__(self, socket):
        self.socket = socket

        lst = Player.id_list
        for i in range(len(lst)):
            if lst[i] != i:
                self.id = i
                break
        else:
            self.id = Player.p_count

        lst.append(self.id)
        lst.sort()
        Player.p_count += 1

    def __del__(self):
        Player.id_list.remove(self.id)
        Player.p_count -= 1

