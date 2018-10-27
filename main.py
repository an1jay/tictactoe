from game import TicTacToe
from player import RandomPlayer
from player import HumanPlayer

if __name__ == '__main__':
    p1 = HumanPlayer()
    p2 = RandomPlayer()
    t = TicTacToe(p1,p2, True)
    t.play()
