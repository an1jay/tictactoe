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
        board_states = np.vstack(
            [board.tryMove(m) for m in board.legalMoves()]
        )
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

    def move(self, board):
        def h(b):
            gameover, winner = b.isGameOver()
            # print("eval at ", b.state, "\n", gameover, winner)
            if gameover:
                if winner is None:
                    return 0
                else:
                    return 2 - 4 * winner
            else:
                return self.evaluator.evaluate(b.state.copy().reshape((1, 19)))

        def minimax(brd, depth, maxplayer):
            MAXVAL = 100000
            gameover, winner = brd.isGameOver()
            if depth == 0 or gameover:
                return h(brd)
            if maxplayer:
                value = -MAXVAL
                for m in brd.legalMoves():
                    new_board = Board(brd.state.copy())
                    new_board.pushMove(m)
                    value = max(value, minimax(new_board, depth - 1, False))
                return value
            else:
                value = MAXVAL
                for m in brd.legalMoves():
                    new_board = Board(brd.state.copy())
                    new_board.pushMove(m)
                    value = min(value, minimax(new_board, depth - 1, True))
                return value

        move_scores = {}
        mxPl = board.state[18] == Board.BLACK_MOVE
        for move in board.legalMoves():
            val = minimax(Board(board.tryMove(move)), self.DEPTH, mxPl)
            # print(board.state, move, val, self.DEPTH, mxPl)
            move_scores[move] = val
        if board.state[18] == Board.WHITE_MOVE:
            return max(move_scores.keys(), key=lambda x: move_scores[x])
        else:
            return min(move_scores.keys(), key=lambda x: move_scores[x])
