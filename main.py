import os
import numpy as np
import time
#from generate import generateExamples
from game import TicTacToe
from player import BasicAIPlayer
from player import HumanPlayer
from player import RandomPlayer
from player import SophisticatedRandomPlayer
from progress import progress
from train import Evaluator

if __name__ == "__main__":
    filename ='example_10k.pkl'
    if not os.path.isfile(filename):
        filename = generateExamples(int(1e5))
    e = Evaluator((27,'relu',27,'relu',27,'tanh',1),loss='mean_squared_error',optimizer='adam')
    f = Evaluator((27,'tanh',27,'tanh',27,'tanh',1),loss='mean_squared_error',optimizer='adam')
    
    for ev in [e,f]:
        if not os.path.isfile(ev.filename()):
            ev.load_data(filename)
            ev.fit()
            ev.save_model()
        else:
            ev.load_model(ev.filename())
     
    scores = np.zeros((2,3)) 
    players = (BasicAIPlayer(e), SophisticatedRandomPlayer())
    for i in range(1000):
        if i%20 == 0:
            progress(i , 1000, status="Playing Games")
        x = np.random.randint(0,2)
        p1 = players[x]
        p2 = players[1-x]
        t = TicTacToe(p1, p2, verbose = False)
        winner = t.play()
        scores[x][1+winner] += 1
        
    print(scores)
        