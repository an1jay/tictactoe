import os
import numpy as np
import time
from generate import generateExamples
from game import TicTacToe
from player import HumanPlayer
from player import SophisticatedRandomPlayer
from player import RandomPlayer
from train import Evaluator

if __name__ == "__main__":
    filename ='example_100k.pkl'
    if not os.path.isfile(filename):
        filename = generateExamples(int(1e5))
    e = Evaluator()
    print(e.evaluate(np.zeros((18))))

    e.load_data(filename)
    e.fit()
    print(e.evaluate(np.zeros((18))))

