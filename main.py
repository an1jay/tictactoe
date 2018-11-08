import os
import numpy as np
import time

# from generate import generateExamples
from game import TicTacToe
from generate import generateExamples
from match import Match
from player import BasicAIPlayer
from player import BasicMMAIPlayer
from player import HumanPlayer
from player import RandomPlayer
from player import SophisticatedRandomPlayer
from progress import progress
from tensorflow import keras
from train import Evaluator

if __name__ == "__main__":
    filename = os.path.join("data", "balanced_example_1k.pbz2")
    if not os.path.isfile(filename):
        filename = generateExamples(int(1e3))
    e = Evaluator(
        (64, "tanh", 16, "tanh", 1),
        loss="mean_absolute_percentage_error",
        optimizer="adam",
    )
    f = Evaluator(
        (64, "tanh", 64, "tanh", 1),
        loss="mean_absolute_error",
        optimizer="adam",
    )
    g = Evaluator(
        (9, "relu", 9, "relu", 9, "relu", 1),
        loss="mean_absolute_percentage_error",
        optimizer="adam",
    )
    h = Evaluator(
        (9, "tanh", 9, "tanh", 9, "tanh", 1),
        loss="mean_absolute_percentage_error",
        optimizer="adam",
    )

    aiplayers = []
    for ev in [e, f, g, h]:
        if not os.path.isfile(ev.filename()):
            print("Found Files")
            ev.load_data(filename)
            ev.fit(epochs=5, batch_size=256)
            ev.save_model()
        else:
            ev.load_model(ev.filename())
        aiplayers.append(BasicMMAIPlayer(ev))

    s = SophisticatedRandomPlayer()
    for p in aiplayers:
        m = Match(p, s)
        print("\nMatch: {} \n".format(p.evaluator.name()), m.play(1000))
    keras.backend.clear_session()
