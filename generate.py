import time
from game import TicTacToe
from player import SophisticatedRandomPlayer
from progress import progress
import bz2
import numpy as np
import os
import pickle
import random


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
            progress(i, numGames, status='Generating games')
    filename = os.path.join('data', f'unbalanced_example_{numGames // 1000}k.pbz2')
    with open(filename, 'wb') as f:
        pickle.dump((x_train, y_train), f)
    return filename


def generateBalancedExamples(numGames):
    p1 = SophisticatedRandomPlayer()
    p2 = SophisticatedRandomPlayer()
    x_train, y_train = [], []
    for i in range(numGames):
        t = TicTacToe(p2, p1, verbose=False, recordGame=True)
        result = t.play()
        x_train.extend(t.gameHistory)
        y_train.extend([result] * len(t.gameHistory))
        if i % 1000 == 0:
            progress(i, numGames, status='Generating games')
    filename = os.path.join('data', f'balanced_example_{numGames // 1000}k.pbz2')

    train = zip(x_train, y_train)
    remove_prob = np.sum(y_train) / np.sum(np.array(y_train) == 1)
    filtered_train = list(
        filter(
            lambda x: not (np.random.random() < remove_prob and x[1] == 1),
            train,
        )
    )

    balanced_x, balanced_y = zip(*filtered_train)

    with bz2.open(filename, 'wb') as f:
        pickle.dump((balanced_x, balanced_y), f)
    return filename


generateBalancedExamples(1_000)
