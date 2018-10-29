import os
import numpy as np
import time
# from generate import generateExamples
from game import TicTacToe
from match import Match
from player import BasicAIPlayer
from player import HumanPlayer
from player import RandomPlayer
from player import SophisticatedRandomPlayer
from progress import progress
from tensorflow import keras
from train import Evaluator

if __name__ == "__main__":
    filename = "balanced_example_150k.pkl"
    if not os.path.isfile(filename):
        filename = generateExamples(int(1e5))
    e = Evaluator(
        (64, "tanh", 64, "tanh", 1), loss="mean_squared_error", optimizer="adam"
    )
    f = Evaluator(
        (64, "tanh", 64, "tanh", 1), loss="mean_absolute_error", optimizer="adam"
    )
    g = Evaluator(
        (27, "tanh", 27, "tanh", 27, "tanh", 1), loss="mean_absolute_error", optimizer="adam"
    )
    h = Evaluator(
        (9, "tanh", 9, "tanh", 9, "tanh", 1), loss="mean_absolute_error", optimizer="adam"
    )

    aiplayers = []
    for ev in [e, f, g, h]:
        if not os.path.isfile(ev.filename()):
            ev.load_data(filename)
            ev.fit(epochs = 3, batch_size = 256)
            ev.save_model()
        else:
            ev.load_model(ev.filename())
        aiplayers.append(BasicAIPlayer(ev))
        
    s = SophisticatedRandomPlayer()
    for p in aiplayers:
        m = Match(p, s)
        print("\nMatch 1: ", m.play(2000))
    

    keras.backend.clear_session()
