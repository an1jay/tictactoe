import os
import numpy as np
import time
from game import TicTacToe
from generate import generateExamples
from match import Match
from player import HumanPlayer
from player import MCTSPlayer
from player import GameTree
from player import MinimaxPlayer
from player import PositionalPlayer
from player import RandomPlayer
from player import SophisticatedRandomPlayer
from progress import progress
# from tensorflow import keras
# from train import Evaluator

if __name__ == "__main__":

    # e = Evaluator(
        # (16, "tanh", 16, "tanh", 1),
        # loss="mean_squared_error",
        # optimizer="adam",
    # )
    # e.load_model("model/16-tanh-16-tanh-1-mean_squared_error.h5")
    


    m = MCTSPlayer(numplayouts = 100, movetime = 4)
    r = SophisticatedRandomPlayer()
    t = TicTacToe(r, m, verbose = True)
    print(t.play())

    # g = GameTree()
    # g.add_node(node = ">", data = "none", parent = None)
    # g.add_node(node = "1", data = "none", parent = ">")
    # g.add_node(node = "0", data = "none", parent = ">1")
    # print(g.get_parents_to_root(">10"))

   
    # match = Match(m , r, False)
    # print(match.play(20))
    
    # keras.backend.clear_session()
    