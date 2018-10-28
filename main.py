import time
from game import TicTacToe
from player import RandomPlayer
from player import HumanPlayer
from player import SophisticatedRandomPlayer

if __name__ == '__main__':
    p1 = SophisticatedRandomPlayer()
    # p1 = HumanPlayer()
    p2 = SophisticatedRandomPlayer()
    reslist = []
    t0 = time.time()
    for i in range(100000):
        t = TicTacToe(p2,p1, verbose=False)
        reslist.append(t.play())
    for val in set(reslist):
        print(val, reslist.count(val))
    print(time.time()-t0)
