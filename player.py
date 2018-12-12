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

# class GameTreeNode:
#     def __init__(self, data = None):
#         self.data = data
#         self.children = []

#     def add_child(self, child):
#         assert isinstance(child, GameTreeNode)
#         self.children.append(child)

#     def update_data(self, new_data):
#         self.data = new_data

#     def __repr__(self):
#         return "Game tree node " + str(self.data)

# MCTStuple = namedtuple('MCTStuple', ['move', 'score', 'numvisits'])


class GameTree:
    def __init__(self):
        self.d = dict()

    def add_node(self, node, data, parent):
        # nodeand parent are str
        # each data is a list [score, numVisits]
        if parent is None:
            assert node == MCTSPlayer.rootnode
            self.d[node] = data
        else:
            # print(self.d.keys())
            assert parent in self.d.keys()
            self.d[parent+node] = data

    def get_parent(self, node):
        # print("Node: ", node)
        # print("keys: ", list(self.d.keys()))
        assert node in self.d.keys()
        return node[:-1]

    def get_parents_to_root(self, node):
        parents = [node]
        p = None
        c = node
        while True:
            if p == MCTSPlayer.rootnode:
                break
            p = self.get_parent(c)
            parents.append(p)
            c = p
        return parents

    def get_data(self, node):
        assert node in self.d
        return self.d[node]

    def update_data(self, node, data):
        assert node in self.d
        self.d[node] = data

    def get_children(self, parent):
        return list(filter(lambda can: parent == self.get_parent(can), self.d.keys()))


class MCTSPlayer(Player):
    rootnode = ">"

    def __init__(self, ep=np.sqrt(2), numplayouts=20,  movetime=45):
        #self.gt = GameTree()
        self.ep = ep
        self.numpl = numplayouts
        self.movet = movetime
        self.p1 = SophisticatedRandomPlayer()
        self.game = TicTacToe(self.p1, self.p1, verbose=False)

    def move(self, board):
        self.gt = GameTree()
        # print("MCTS moveS")
        t0 = time.time()

        # which player are we?
        p = board.state[18]

        # define root node (i.e. current game state)
        self.gt.add_node(node=MCTSPlayer.rootnode, data=[0, 0], parent=None)

        # add children of root node
        for m in board.legalMoves():
            self.gt.add_node(node=str(m), data=[
                             0, 0], parent=MCTSPlayer.rootnode)

        player = board.state[18]

        while True:
            # print("in while loop")
            chosennode = self.choose_next_node(MCTSPlayer.rootnode, board)
            # print("CHosen NodE", chosennode)

            if time.time() - t0 > self.movet:
                break
            nodeboard = Board(board.state.copy())
            for m in chosennode[1:]:
                nodeboard.pushMove(int(m))

            score = self.playout(nodeboard, player)

            # back propagate score & numVisits
            for node in self.gt.get_parents_to_root(chosennode):
                data = self.gt.get_data(node)
                data[0] += score
                data[1] += 1
                self.gt.update_data(node, data)

            for m in nodeboard.legalMoves():
                self.gt.add_node(str(m), data=[0, 0], parent=chosennode)

        best_move = None
        best_numVisits = 0
        for m in self.gt.get_children(MCTSPlayer.rootnode):
            data = self.gt.get_data(m)
            if data[1] > best_numVisits:
                best_numVisits = data[1]
                best_move = m
        # return max(self.gt.get_children(MCTSPlayer.rootnode), key = lambda m: self.gt.get_data(m)[1])
        # print('children visits', list(map(lambda x: (x,self.gt.get_data(x)[1]), self.gt.get_children(MCTSPlayer.rootnode))))
        return int(best_move[1])

    def playout(self, board, player):
        gameover, winner = board.isGameOver()
        if gameover:
            if winner is None:
                return 0
            elif winner == player:
                return 1
            else:
                return -1
        scr = 0
        for _ in range(self.numpl):
            self.game.board = Board(board.state.copy())
            scr += self.game.play() * (1-2*player)
        return scr/self.numpl

    def choose_next_level_node(self, currnode, board):
        # returns node, Terminal (bool)
        
        children = self.gt.get_children(currnode)
        childUCTs = list(
            map(lambda cnode: self.calcUCT(currnode, cnode, ), children))
        bestUCT = -1e6
        bestchild = "-------------"

        for index in range(len(childUCTs)):
            terminal = self.is_node_terminal(children[index], board)
            if childUCTs[index] is None:
                # print("Child has None UCT index", index, 'child', children[index], 'child unct', childUCTs[index])
                return children[index], terminal
            elif childUCTs[index] > bestUCT:
                # print("Child has not None UCT, index", index, 'child', children[index], 'child unct', childUCTs[index])
                bestUCT = childUCTs[index]
                bestchild = children[index]
                # print('bestchild', bestchild)
        return bestchild, terminal

    def choose_next_node(self, currnode, board):
        parent = currnode
        # Equiv to  while TRUE; maybe change?
        for _ in range(9):
            node, terminal = self.choose_next_level_node(parent, board)
            # print('choose_next_node: node ', node, 'terminal ', terminal)
            if terminal:
                return node
            else:
                parent = node

    def is_node_terminal(self, node, rootboard):
        # returns terminal, winner at current node

        bd = Board(rootboard.state.copy())
        for m in node[1:]:
            bd.pushMove(int(m))
        gameover, _ = bd.isGameOver()
        if gameover:
            # print("GameOver True")
            return True
        elif self.gt.get_data(node)[1] == 0:
            # print("GameOver False, 0 Visits True")
            return True
        else:
            return False

    def calcUCT(self, parentnode, childnode):
        if self.gt.get_data(childnode)[1] == 0:
            return None
        return self.gt.get_data(childnode)[0]/self.gt.get_data(childnode)[1] + self.ep * np.sqrt(np.log(self.gt.get_data(parentnode)[1])/self.gt.get_data(childnode)[1])
