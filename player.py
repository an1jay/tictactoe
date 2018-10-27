import numpy as np

class Player:
    def __init__(self):
        pass

    def move(self):
        pass

    def reward(self, value):
        pass

    def startGame(self):
        pass


class QLearningPlayer(Player):
    def __init__(self):
        pass

    def move(self):
        pass

    def reward(self):
        pass

class RandomPlayer(Player):
    def move(self, board):
        return np.random.randint(9)

class HumanPlayer(Player):
    def move(self, board):
        i_move = input("Insert move (0-8)")
        while i_move not in range(9):
            i_move = input("Inset move (0-8)")
        return i_move

