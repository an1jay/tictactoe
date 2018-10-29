import os
import numpy as np
import time

try:
    import keras
except e:
    pass
# from generate import generateExamples
from game import TicTacToe
from match import Match
from player import BasicAIPlayer
from player import HumanPlayer
from player import RandomPlayer
from player import SophisticatedRandomPlayer
from progress import progress
from train import Evaluator

if __name__ == "__main__":
    filename = "example_100k.pkl"
    if not os.path.isfile(filename):
        filename = generateExamples(int(1e5))
    e = Evaluator(
        (30, "relu", 27, "tanh", 1), loss="mean_squared_error", optimizer="adam"
    )
    f = Evaluator(
        (30, "relu", 27, "tanh", 1, "tanh"), loss="mean_squared_error", optimizer="adam"
    )

    for ev in [e, f]:
        if not os.path.isfile(ev.filename()):
            ev.load_data(filename)
            ev.fit()
            ev.save_model()
        else:
            ev.load_model(ev.filename())

    scores = np.zeros((2, 3))
    be = BasicAIPlayer(e)
    bf = BasicAIPlayer(f)
    s = SophisticatedRandomPlayer()
    m1 = Match(be, s)
    m2 = Match(bf, s)
    print("\nMatch 1: ", m1.play(100))
    print("\nMatch 2: ", m2.play(100))

    keras.backend.clear_session()
