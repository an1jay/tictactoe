import time
from game import TicTacToe
from player import SophisticatedRandomPlayer
from progress import progress
import pickle


def generateExamples(numGames):
    p1 = SophisticatedRandomPlayer()
    p2 = SophisticatedRandomPlayer()
    x_train, y_train = [], []
    for i in range(numGames):
        t = TicTacToe(p2, p1, verbose=False, recordGame=True)
        result = t.play()
        x_train.extend(t.gameHistory)
        y_train.extend([result] * len(t.gameHistory))
        if i % 1000 == 0:
            progress(i, numGames, status="Generating games")
    filename = f"example_{numGames//1000}k.pkl"
    with open(filename, "wb") as f:
        pickle.dump((x_train, y_train), f)
    return filename
