import os
import numpy as np
import time
from game import TicTacToe
from generate import generateExamples
from match import Match
from player import HumanPlayer
from player import MCTSPlayer
from player import GameTree
from player import MinimaxPlayer
from player import PositionalPlayer
from player import RandomPlayer
from player import SophisticatedRandomPlayer
from progress import progress
# from tensorflow import keras
# from train import Evaluator

if __name__ == "__main__":

    # e = Evaluator(
        # (16, "tanh", 16, "tanh", 1),
        # loss="mean_squared_error",
        # optimizer="adam",
    # )
    # e.load_model("model/16-tanh-16-tanh-1-mean_squared_error.h5")

    # m = MCTSPlayer(numplayouts = 20, movetime = 1)
    # r = SophisticatedRandomPlayer()
    # match = Match(m , r, False)
    # print(match.play(20))
    # m = MCTSPlayer(numplayouts = 20, movetime = 2)
    # r = SophisticatedRandomPlayer()
    # # t = TicTacToe(r, m, verbose = True)
    # # print(t.play())

    # # g = GameTree()
    # # g.add_node(node = ">", data = "none", parent = None)
    # # g.add_node(node = "1", data = "none", parent = ">")
    # # g.add_node(node = "0", data = "none", parent = ">1")
    # # print(g.get_parents_to_root(">10"))

    # keras.backend.clear_session()

    # m = MCTSPlayer(numplayouts = 20, movetime = 10, ep = 1.4142135623730950488)

    # m = MinimaxPlayer(ev=None, depth=9)
    # t = TicTacToe(r, m, verbose = True)
    # print(t.play())
    m = HumanPlayer()

    dic = {}


    unit = 1.414
    r = MCTSPlayer()

    match = Match(r, m, True)
    res = match.play(10)
    dic[unit] = res
    
    print(dic)

    # m.startGame()
    # b = Board()
    # b.pushMove(0)
    # b.pushMove(2)
    # b.pushMove(3)
    # b.pushMove(4)
    # b.pushMove(6)
    # print(m.board_already_in_gt(b))
    # print("B state", b.state)05

    # r = SophisticatedRandomPlayer()
    # match = Match(m , r, True)
    # print(match.play(2))
