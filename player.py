import numpy as np
import random
import time
from collections import namedtuple
from collections import OrderedDict
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
        # print(self.__class__.__name__, "starts game")
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
    def __init__(self, ev, depth, cachelimit=int(1000)):
        self.evaluator = ev
        self.DEPTH = depth
        self.nodecount = 0
        self.cache = {}
        self.cachelimit = cachelimit
    
    def startGame(self):
        print("MinimaxPlayer starts game")

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
            self.increment_nodecount()
            MAXVAL = 100000
            gameover, _ = brd.isGameOver()
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

        t0 = time.time()

        print("MinimaxPlayer thinks...")
        # if move in cache, play it
        # print("MMP - pre - cache: ", self.cache)
        if tuple(board.state) in self.cache.keys():
            print("MinimaxPlayer depth {0} played from cache in {1:.2f} seconds".format(
                self.DEPTH, time.time()-t0))
            return self.cache[tuple(board.state)]

        move_scores = {}
        mxPl = board.state[18] == Board.BLACK_MOVE
        for move in board.legalMoves():
            val = minimax(Board(board.tryMove(move)), self.DEPTH, mxPl)
            # print(board.state, move, val, self.DEPTH, mxPl)
            move_scores[move] = val
        time_elapsed = time.time()-t0
        try:
            ncnt = self.nodecount/time_elapsed
        except ZeroDivisionError:
            ncnt = 1e9
        print("MinimaxPlayer depth {0} explored {1} nodes in {2:.2f} seconds at {3:.2f} nodes/s".format(
            self.DEPTH, self.nodecount, time_elapsed, ncnt))
        self.reset_nodecount()
        if board.state[18] == Board.WHITE_MOVE:
            bmove = max(move_scores.keys(), key=lambda x: move_scores[x])
            # while cache is smaller than cache limit, add move to cache
            if len(self.cache.keys()) < self.cachelimit:
                self.cache[tuple(board.state)] = bmove
                # print("MMP - post - cache: ", self.cache)
            return bmove
        else:
            bmove = min(move_scores.keys(), key=lambda x: move_scores[x])
            # while cache is smaller than cache limit, add move to cache
            if len(self.cache.keys()) < self.cachelimit:
                self.cache[tuple(board.state)] = bmove
                # print("MMP - post - cache: ", self.cache)
            return bmove

    def increment_nodecount(self):
        self.nodecount += 1

    def reset_nodecount(self):
        self.nodecount = 0


class MCTSPlayer(Player):
    rootnode = ">"

    def __init__(self, ep=np.sqrt(2), numplayouts=20,  movetime=45):
        self.gt = GameTree()
        self.ep = ep
        self.numpl = numplayouts
        self.movet = movetime
        self.p1 = SophisticatedRandomPlayer()
        self.game = TicTacToe(self.p1, self.p1, verbose=False)

    def startGame(self):
        print("MCTSPlayer starts game")
        self.gt = GameTree()
        # define root node (i.e. current game state)
        self.gt.add_node(node=MCTSPlayer.rootnode, data=[0, 0], parent=None)

    def move(self, board):
        print("MCTSPlayer thinks...")
        nodecnt = 0
        t0 = time.time()
        rtnode, alrdy_in = self.board_already_in_gt(board)
        # print("RTNODE: ", rtnode)
        # node not in; if node in, no need to do anything
        if not alrdy_in:
            # need to check if any parents are in gt.
            rtnode_would_be_parents = self.gt.get_would_be_parents_to_root(
                rtnode)

            # get parent in game tree, not grandparent, etc
            # print("RTNode parents", rtnode_would_be_parents)
            last_parent_in_gt = max(list(filter(lambda x: self.gt.node_in_tree(
                x), rtnode_would_be_parents)), key=lambda x: len(x))
            # print("Latest parent: ", last_parent_in_gt)
            # print("Parent - RTnode", rtnode.replace(last_parent_in_gt, ""))

            # add all children of that parent
            last_added_parent = last_parent_in_gt
            for m in rtnode.replace(last_parent_in_gt, ""):
                # print("adding: ", m, "with parent: ", last_added_parent)
                self.gt.add_node(m, [0, 0], last_added_parent)
                last_added_parent = last_added_parent + m

        # which player are we?
        player = board.state[18]

        while True:
            nodecnt += 1
            # print("RTNODE in WHile LOOP: ", rtnode)
            chosennode = self.choose_next_node(rtnode, board)
            if time.time() - t0 > self.movet:
                break
            nodeboard = Board(board.state.copy())
            for m in chosennode.replace(rtnode, ""):
                nodeboard.pushMove(int(m))

            # Add children of current node
            for m in nodeboard.legalMoves():
                self.gt.add_node(str(m), data=[0, 0], parent=chosennode)

            score = self.playout(nodeboard, player)

            # back propagate score & numVisits
            # print("Chosen Node: '" + chosennode + "'")
            for node in self.gt.get_parents_to_root(chosennode):
                data = self.gt.get_data(node)
                data[0] += score
                data[1] += 1
                self.gt.update_data(node, data)

        best_move = None
        best_numVisits = 0
        for m in self.gt.get_children(rtnode):
            data = self.gt.get_data(m)
            if data[1] > best_numVisits:
                best_numVisits = data[1]
                best_move = m
        # return max(self.gt.get_children(MCTSPlayer.rootnode), key = lambda m: self.gt.get_data(m)[1])
        # print("node", rtnode, 'children visits', list(map(lambda x: (x,self.gt.get_data(x)[1]), self.gt.get_children(rtnode))))
        print("MCTSPLayer explored {0} nodes in {1} seconds at {2:.2f} nodes/s".format(
            nodecnt, self.movet, nodecnt/self.movet))
        return int(best_move[-1])

    def board_already_in_gt(self, board):
        # returns most visited node if the board position input is already in the gt, and whether the node is in game tree
        num_moves = np.sum(board.state[:18])
        possibilities = filter(lambda x: len(
            x) == num_moves + 1, self.gt.get_all_nodes())
        equivalents = []
        for p in possibilities:
            b = Board()
            for m in p[1:]:
                b.pushMove(int(m))
            if np.array_equal(b.state, board.state):
                equivalents.append(p)

        if len(equivalents) == 0:
            bdarray = board.state.copy()[:-1]
            where1 = list(np.where(bdarray[:9] == 1)[0])
            where2 = list(np.where(bdarray[9:] == 1)[0])
            node = []
            for i in range(min(len(where1), len(where2))):
                print("I:", i)
                node.append(str(where1[i]))
                node.append(str(where2[i]))
            if len(where1) > len(where2):
                node.append(str(where1[-1]))
            node = "".join(node)
            node = MCTSPlayer.rootnode + node.strip()
            return node, False
        else:
            return max(equivalents, key=lambda x: self.gt.get_data(x)[1]), True

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
        if len(children) == 0:
            return currnode, True
        childUCTs = list(
            map(lambda cnode: self.calcUCT(currnode, cnode, ), children))
        bestUCT = -1e6
        bestchild = "-------------"
        # print("children: ", children)
        # print("childUCTS: ", childUCTs)
        #terminal = True
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

        try:
            assert node in self.d.keys()
        except:
            print("Invalid node: `" + node + "`")
            raise AssertionError

        return node[:-1]

    def get_would_be_parent(self, node):
        return node[:-1]

    def get_parents_to_root(self, node):
        if node == ">":
            return ">"
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

    def get_would_be_parents_to_root(self, node):
        parents = [node]
        p = None
        c = node
        while True:
            if p == MCTSPlayer.rootnode:
                break
            p = self.get_would_be_parent(c)
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

    def get_all_nodes(self):
        return self.d.keys()

    def node_in_tree(self, node):
        return node in self.d.keys()
