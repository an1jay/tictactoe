import time
from game import TicTacToe
from player import SophisticatedRandomPlayer
from progress import progress
import bz2
import math
import numpy as np
import os
import pickle
import random


def generateExamples(p1, p2, numGames, ext="", save=True):
    # p1 plays p2 numGames times and the gamehistory
    # and result of the games are returned as two numpy arrays
    filename = os.path.join(
        "data", "u_games_{}k".format(numGames // 1000) + ext + ".pbz2"
    )
    if os.path.isfile(filename):
        return filename
    x_train = []
    y_train = []
    for i in range(numGames):
        t = TicTacToe(p1, p2, verbose=False)
        result = t.play()
        x_train.append(t.board.gameHistory)
        y_train.extend([result] * len(t.board.gameHistory))
        if i % math.ceil(0.01 * numGames) == 0:
            progress(i, numGames, status="Generating games")
    x_t = np.vstack(x_train)
    y_t = np.array(y_train)
    if save:
        with bz2.open(filename, "wb") as f:
            pickle.dump((x_t, y_t), f)
        return filename
    else:
        return (x_t, y_t)


def generateBalancedExamples(p1, p2, numGames, save=True):
    # p1 plays p2 numGames times and the gamehistory and result of the
    # games are 'balanced' (i.e. result ends up where p1 and p2 win
    # the same amount on average) and the returned as 2 numpy arrays
    filename = os.path.join(
        "data", "b_games_{}k.pbz2".format(numGames // 1000)
    )
    if os.path.isfile(filename):
        return filename
    x_train, y_train = generateExamples(p1, p2, numGames, save=False)
    train = zip(x_train, y_train)
    remove_prob = np.sum(y_train) / np.sum(np.array(y_train) == 1)
    filtered_train = list(
        filter(
            lambda x: not (np.random.random() < remove_prob and x[1] == 1),
            train,
        )
    )
    balanced_x, balanced_y = zip(*filtered_train)
    if save:
        with bz2.open(filename, "wb") as f:
            pickle.dump((balanced_x, balanced_y), f)
        return filename
    else:
        return (balanced_x, balanced_y)
