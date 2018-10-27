from game import TicTacToe
from player import RandomPlayer

if __name__ == '__main__':
    p1 = RandomPlayer()
    p2 = RandomPlayer()
    t = TicTacToe(p1,p2, True)
    t.play()
