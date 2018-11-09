import os
import numpy as np
import time
from game import TicTacToe
# from generate import generateExamples
from match import Match
from player import HumanPlayer
from player import MinimaxPlayer
from player import PositionalPlayer
from player import RandomPlayer
from player import SophisticatedRandomPlayer
from progress import progress
from tensorflow import keras
from train import Evaluator

if __name__ == "__main__":
    
    ev = Evaluator(
        (64, "tanh", 16, "tanh", 1),
        loss="mean_absolute_error",
        optimizer="adam",
    )
    ev.load_model(ev.filename())
    b = PositionalPlayer(ev)
    # s = BasicAIPlayer(ev)
    # s = SophisticatedRandomPlayer()
    # m = Match(b, s, True)
    # print(m.play(10))
    
    a = HumanPlayer()
    TicTacToe(b, a, verbose = True).play()
    
    keras.backend.clear_session()
