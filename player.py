import numpy as np
import random

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

class SophisticatedRandomPlayer(Player):
    def move(self, board):
        choices = []
        for i in range(9):
            if board[0,i]+board[1,i] == 0:
                choices.append(i)
        return random.choice(choices)

class HumanPlayer(Player):
    def move(self, board):
        i_move = -1
        while i_move not in range(9):
            try:
                i_move = int(input("Insert move (0-8)"))
            except e:
                pass
        print()
        return i_move

