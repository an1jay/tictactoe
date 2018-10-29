import time
from game import TicTacToe
from player import RandomPlayer
from player import HumanPlayer
from player import SophisticatedRandomPlayer
from train import Evaluator
import numpy as np

if __name__ == "__main__":
    e = Evaluator()
    print(e.evaluate(np.zeros((18))))

    e.load_data("positiontrain_100k_862425.pkl")
    e.fit()
    print(e.evaluate(np.zeros((18))))
