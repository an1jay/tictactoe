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
            gameover, winner = brd.isGameOver()
            
            if gameover and (winner is None):
                return 0
            elif gameover:
                return - 10(1 - 2*winner)        
            if depth == 0:
                if gameover and (winner is None):
                    return 0
                elif gameover:
                    return - 10(1 - 2*winner)
                else:
                    return self.evaluator.evaluate(board.state.copy().reshape((1,19)))
                
            if board.state[18]:
                value = -MAXVAL
                for m in board.legalMoves():
                    bd = Board(board.state.copy())
                    bd.pushMove(m)
                    value = max(value, minimax(bd, depth-1))
                return value
            else:
                value = MAXVAL
                for m in board.legalMoves():
                    bd = Board(board.state.copy())
                    bd.pushMove(m)
                    value = min(value, minimax(bd, depth-1))
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
            gameover, winner = b.isGameOver()
            if gameover and winner == 1 - b.state[18]:
                return i
        # print(brd.legalMoves(), " ---- ", move_scores)
        if brd.state[18] == 1:
            return move_location[np.argmax(move_scores)]
        else:
            return move_location[np.argmin(move_scores)]

class MinimaxPlayer2(Player):
    def __init__(self, depth, ev = None):
        self.evaluator = ev
        self.DEPTH = depth

    def move(self, brd):
        def v(b2, move):
            return self.evaluator.evaluate(b2.tryMove(move).reshape((1,19)))
        moves = {}
        
        
        for m1 in brd.legalMoves():
            b = Board(brd.state.copy())
            b.pushMove(m1)
            gameover, winner = b.isGameOver()
            if gameover and winner == 1 - b.state[18]:
                return m1
            
            scores = []
            for m2 in b.legalMoves():
                b2 = Board(b.state.copy())
                b2.pushMove(m2)
                
                scores2 = [v(b2, m2) for m2 in b.legalMoves()]
                if len(scores2) == 0:
                    scores2 = [0]
                if brd.state[18] == 0:
                    scores.append(min(scores2))
                else:
                    scores.append(max(scores2))
                
            if len(scores) == 0:
                scores = [0]
            
            if brd.state[18] == 0:    
                moves[m1] = max(scores)
            else:
                moves[m1] = min(scores)
                
        if brd.state[18] == 0:
            return min(moves, key = lambda x: moves[x])
        else: 
            return max(moves, key = lambda x: moves[x])
        
