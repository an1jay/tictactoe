from collections import namedtuple
import numpy as np
import random
import time
from game import Board
from game import TicTacToe


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
            except:
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

# class MCTSPlayer(Player):
    # def __init__(self, playouts = 50, exploration_parameter = np.sqrt(2), movetime = 30):
        # self.playouts = playouts
        # # self.gametree = GameTreeNode(data = MCTStuple(None, 0, 0))    
        # self.randomplayer = SophisticatedRandomPlayer()
        # self.game = TicTacToe(self.randomplayer, self.randomplayer, verbose = False)
        # self.ep = exploration_parameter
        # self.movetime = movetime

    # def move(self, board):
        # mctsplayer = board.state[18]
        # print(mctsplayer)
        # def chooseNode(node, pl): # using UCT or randomly picking an unvisited child node
            # if node is None:
                # return None, False
            # best_child = None
            # best_UCT = -1000000
            # for child in node.children:
                # if child.data.numvisits == 0:
                    # return child, False
                # else:
                    # try:
                        # UCT = ((-1)**pl)*child.data.score / child.data.numvisits + self.ep * np.sqrt(np.log(node.data.numvisits) / child.data.numvisits)
                    # except ZeroDivisionError:
                        # print("MCTS: move: chooseNode: UCT being calculated for unvisited node")
                        # pass
                    # if UCT > best_UCT:
                        # best_UCT = UCT
                        # best_child = child
                        # print(best_UCT)
            
            # return best_child, True
        
        # def playout(b):
            # isgo, winner = b.isGameOver()
            # if isgo and winner is not None:
                # return (1 - 2 * winner) * self.playouts
            # elif isgo:
                # return 0
            # q = 0
            # for _ in range(self.playouts):
                # self.game.board = Board(b.state.copy())
                # q += self.game.play()
                # # self.game.reset()
            # return q   
        
        # rootnode = GameTreeNode(data = MCTStuple(-1, 0, 1))
        # for m in board.legalMoves():
                # rootnode.add_child(GameTreeNode(data = MCTStuple(m,0,0)))
        # t0 = time.time()
        # while True:
            # bd = Board(board.state.copy())
            # node = rootnode
            # history = [node]
            # visited = node.data.numvisits != 0 # true iff node is visited
            # # print("MCTS move(): in while loop TRUE          ", node)
            # while visited: # finds an unvisited node and stores the path to get there
                # # print("MCTS move(): in while loop visited (pre) ", node)
                # if not (node is None):
                    # node, visited = chooseNode(node, bd.state[18])
                    # if not (node is None):
                        # history.append(node)
                        # bd.pushMove(node.data.move)
                        # winner, isgameover = bd.isGameOver()
                        # if isgameover:
                            # visited = False
                        # print(list(map(lambda x: (x.data.move, x.data.score, x.data.numvisits), history)))
                # # print("MCTS move(): in while loop visited (post)", node)
            # q_val = playout(bd)/self.playouts
            # for n in history: # backpropagates the score of this unvisited node 
                # n.data.score += q_val
                # n.data.numvisits += 1
            
            # for m in bd.legalMoves():
                # node.add_child(GameTreeNode(data = MCTStuple(m,0,0)))        
            
            # if time.time() - t0 > self.movetime:
                # break
        
        # bn = max(rootnode.children, key = lambda x: x.data.numvisits)
        # return bn.data.move
        
class GameTreeNode:
    def __init__(self, data = None):
        self.data = data
        self.children = []
    
    def add_child(self, child):
        assert isinstance(child, GameTreeNode)
        self.children.append(child)
        
    def update_data(self, new_data):
        self.data = new_data

    def __repr__(self):
        return "Game tree node " + str(self.data)

class MCTStuple:
    def __init__(self, move, score, numvisits):
        self.move = move
        self.score = score
        self.numvisits = numvisits
    
    def __str__(self):
        return "move: " + str(self.move)+" score: " + str(self.score) + " numVisits: " + str(self.numvisits)
            
# MCTStuple = namedtuple('MCTStuple', ['move','score','numvisits'])
        
    
    
    
    
    
    
    
    
        