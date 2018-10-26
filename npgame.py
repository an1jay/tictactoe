import numpy as np

class TicTacToe:
    def __init__(self, player1, player2, rewards, verbose):
        self.p1 = player1
        self.p2 = player2

        self.REWARDS = rewards # tuple (win, loss, draw, inbetweenmove)
        self.VERBOSE = verbose

        self.board = np.zeros((2,9)) # 1st dimension is player 1, 2nd dimension is player 2
    
    def play(self):
        pass

    def isGameOver(self):
        pass


