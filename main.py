from game import TicTacToe
from player import RandomPlayer
from player import HumanPlayer
from player import SophisticatedRandomPlayer

if __name__ == '__main__':
    p1 = SophisticatedRandomPlayer()
    p2 = SophisticatedRandomPlayer()
    t = TicTacToe(p1,p2, False)
    t.play()
