import time
from game import TicTacToe
from player import RandomPlayer
from player import HumanPlayer
from player import SophisticatedRandomPlayer
import pickle

if __name__ == '__main__':
    n = 100000
    p1 = SophisticatedRandomPlayer()
    # p1 = HumanPlayer()
    p2 = SophisticatedRandomPlayer()
    t0 = time.time()
    
    x_train, y_train = [], []
    for i in range(n):
        t = TicTacToe(p2,p1, verbose=False, recordGame=True)
        result = t.play()
        x_train.extend(t.gameHistory)
        y_train.extend([result]*len(t.gameHistory))
            
    print(time.time()-t0)
    
    with open(f'positiontrain_{n//1000}k_{len(x_train)}.pkl', 'wb') as f:
        pickle.dump((x_train,y_train), f)
