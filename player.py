import numpy as np
import random

from game import Board

class Player:
    def __init__(self):
        pass

    def move(self):
        pass

    def reward(self, value):
        # print(self.__class__.__name__, "has been rewarded", value)
        pass

    def startGame(self):
        pass


class QLearningPlayer(Player):
    def __init__(self):
        pass

    def move(self):
        pass


class RandomPlayer(Player):
    def move(self, board):
        return np.random.randint(9)


class SophisticatedRandomPlayer(Player):
    def move(self, board):
        return random.choice(board.legalMoves())


class HumanPlayer(Player):
    def move(self, board):
        i_move = -1
        while i_move not in range(9):
            try:
                i_move = int(input("Insert move (0-8)"))
            except e:
                pass
        print()
        return i_move


class PositionalPlayer(Player):
    def __init__(self, ev):
        self.evaluator = ev

    def move(self, board):
        board_states = np.vstack([board.tryMove(m) for m in board.legalMoves()])
        move_location = dict(
            zip(range(len(board.legalMoves())), board.legalMoves())
        )
        move_scores = self.evaluator.evaluate(board_states)
        if board.state[18]:
            return move_location[np.argmin(move_scores)]
        else:
            return move_location[np.argmax(move_scores)]


class MinimaxPlayer(Player):
    def __init__(self, ev, depth):
        self.evaluator = ev
        self.DEPTH = depth

    def move(self, brd):
        def minimax(board, depth):
            MAXVAL = 2
            # print(board.state.copy().reshape((1,19)))
            # print(board, "--- depth",  depth)
            if depth == 0:
                return self.evaluator.evaluate(board.state.copy().reshape((1,19)))

            if board.state[18]:
                value = -MAXVAL
                for m in board.legalMoves():
                    board.pushMove(m)
                    value = max(value, minimax(board, depth-1))
                return value
            else:
                value = MAXVAL
                for m in board.legalMoves():
                    board.pushMove(m)
                    value = min(value, minimax(board, depth-1))
                return value

        board_states = np.vstack([brd.tryMove(m) for m in brd.legalMoves()])
        move_location = dict(
            zip(range(len(brd.legalMoves())), brd.legalMoves())
        )
        move_scores = []
        for i in brd.legalMoves():
           b = Board(brd.state.copy())
           b.pushMove(i)
           move_scores.append(minimax(b, self.DEPTH))
        # print(brd.legalMoves(), " ---- ", move_scores)
        return move_location[np.argmax(move_scores)]

class MinimaxPlayer2(Player)
    def __init__(self, ev, depth):
        self.evaluator = ev
        self.DEPTH = depth

    def move(self, brd):
