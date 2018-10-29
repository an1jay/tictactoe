import time
from game import TicTacToe
from player import SophisticatedRandomPlayer
import pickle


def generateExamples(numGames):
    p1 = SophisticatedRandomPlayer()
    p2 = SophisticatedRandomPlayer()
    x_train, y_train = [], []
    for i in range(n):
        t = TicTacToe(p2, p1, verbose=False, recordGame=True)
        result = t.play()
        x_train.extend(t.gameHistory)
        y_train.extend([result] * len(t.gameHistory))
    print(time.time() - t0)
    with open(f"example_{n//1000}k}.pkl", "wb") as f:
        pickle.dump((x_train, y_train), f)
