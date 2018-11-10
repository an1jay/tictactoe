import os
import numpy as np
import time
from game import TicTacToe
from generate import generateExamples
from match import Match
from player import HumanPlayer
from player import MinimaxPlayer2, MinimaxPlayer
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

    filename = generateExamples(
        SophisticatedRandomPlayer(),
        SophisticatedRandomPlayer(),
        int(2.5e4),
        save=True,
    )
    for i in [e]:
        # i.load_data(filename)
        # i.fit(epochs = 2, batch_size=512)
        # i.save_model()
        i.load_model(i.filename())
        print(i.name())
        print(i.evaluate(np.zeros(19).reshape((1,19))))
        a = MinimaxPlayer2(ev = i, depth = 1)
        c = MinimaxPlayer(ev = i, depth = 1)
        # a = PositionalPlayer(i)
        b = SophisticatedRandomPlayer()
        t = TicTacToe(a,c,True)
        t.play()
        # print(t.board.gameHistory, 'full game history')
        print(Match(b,b,False).play(100))        
        print(Match(b,c,False).play(100))
        print(Match(b,a,False).play(100))
    keras.backend.clear_session()
