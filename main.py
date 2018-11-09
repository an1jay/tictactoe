import os
import numpy as np
import time
from game import TicTacToe

from generate import generateExamples
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

    e = Evaluator(
        (16, "tanh", 16, "tanh", 1),
        loss="mean_squared_error",
        optimizer="adam",
    )
    f = Evaluator(
        (64, "tanh", 1), loss="mean_absolute_error", optimizer="adam"
    )
    g = Evaluator(
        (27, "tanh", 27, "tanh", 27, "tanh", 1),
        loss="mean_absolute_error",
        optimizer="adam",
    )
    h = Evaluator(
        (16, "relu", 16, "relu", 1),
        loss="mean_absolute_error",
        optimizer="adam",
    )
    filename = generateExamples(
        SophisticatedRandomPlayer(),
        SophisticatedRandomPlayer(),
        int(2.5e5),
        save=True,
    )
    for i in [e]:
        # i.load_data(filename)
        # i.fit(epochs = 2, batch_size=1024)
        # i.save_model()
        i.load_model(i.filename())
        print(i.name())
        print(i.evaluate(np.zeros(19).reshape((1,19))))
        a = MinimaxPlayer(i, depth = 1)
        # a = PositionalPlayer(i)
        b = SophisticatedRandomPlayer()
        # t = TicTacToe(a,b,True)
        # t.play()
        print(Match(b,b,False).play(1000))
        print(Match(a,b,False).play(1000))
    keras.backend.clear_session()
