import collections
import numpy as np

Reward = collections.namedtuple("Reward", ["win", "loss", "tie", "endofmove"])


class TicTacToe:
    def __init__(self, p1, p2, verbose, rewards=(1, -1, 0.5, 0)):
        self.players = [p1, p2]
        self.REWARDS = Reward(*rewards)
        # tuple (win, loss, draw, inbetweenmove)
        self.VERBOSE = verbose
        self.board = Board()
        # first 9 are player 1, second 9 are player 2, final is whose move it is

    def play(self):
        # returns 1 if p1 wins, -1 if p2 wins, 0 if tie
        for player in self.players:
            player.startGame()

        self.smartPrint(
            "Match between "
            + self.players[0].__class__.__name__
            + " (player 1, 'X') and "
            + self.players[1].__class__.__name__
            + " (player 2, 'O')."
        )
        while True:
            for p in [0, 1]:  # for each player
                self.smartPrint(self.board)
                move = self.players[p].move(self.board)
                self.smartPrint(
                    self.players[p].__class__.__name__ + " played " + str(move)
                )
                if not self.board.isLegalMove(move):
                    # checks if legal move
                    self.players[p].reward(self.REWARDS.loss)
                    self.smartPrint("Illegal move!\n")
                    self.smartPrint(self.board)
                    return 2 * p - 1
                else:
                    self.board.pushMove(move)
                isover, winner = self.board.isGameOver()
                if isover and (not winner is None):
                    self.players[winner].reward(self.REWARDS.win)
                    self.players[1 - winner].reward(self.REWARDS.loss)
                    self.smartPrint(
                        self.players[winner].__class__.__name__
                        + " (player "
                        + str(winner + 1)
                        + ", "
                        + ["X", "O"][winner]
                        + ") won!"
                    )
                    self.smartPrint(self.board)
                    return 1 - 2 * winner
                elif isover and winner is None:
                    self.players[0].reward(self.REWARDS.tie)
                    self.players[1].reward(self.REWARDS.tie)
                    self.smartPrint("Tie!")
                    self.smartPrint(self.board)
                    return 0
                else:
                    self.players[p].reward(self.REWARDS.endofmove)

    def reset(self):
        self.board = Board()
    
    def smartPrint(self, x, ending="\n"):
        if self.VERBOSE:
            print(x, end=ending)


class Board:
    WHITE_MOVE = 0
    BLACK_MOVE = 1

    def __init__(self, b=None):
        if b is None:
            self.state = np.zeros(19, dtype=np.dtype("u8"))
        else:
            self.state = b

        # self.state stores in 18 elements, the board (p1 moves, and p2 moves) and 19th element holds the player to move (0=p1, 1=p2)
        self.previous_state = None
        self.gameHistory = self.state.copy()

    def __repr__(self):
        strbrd = []
        for x, o in zip(self.state[0:9], self.state[9:18]):
            if x:
                char = "X"
            elif o:
                char = "O"
            else:
                char = " "
            strbrd.append(char)
        return "\n".join(
            ["|".join(strbrd[:3]), "|".join(strbrd[3:6]), "|".join(strbrd[6:])]
        )

    def pushMove(self, move):
        player = self.state[18]
        self.state[int(player) * 9 + move] = 1
        self.state[18] = 1 - player
        self.gameHistory = np.vstack(
            [self.gameHistory.copy(), self.state.copy()]
        )

    def popMoves(self, movesback):
        if movesback < self.gameHistory.shape[1]:
            self.state = self.gameHistory[-movesback - 1]
        else:
            raise LookupError("popping too many moves")
        self.gameHistory = self.gameHistory[:-1]

    def tryMove(self, move):
        tempstate = self.state.copy()
        player = tempstate[18]
        tempstate[int(player) * 9 + move] = 1
        tempstate[18] = 1 - player
        return tempstate

    def isGameOver(self):
        # returns Boolean for if the game is over, and 0 if p1 has won, 1 if p2 has won
        winconditions = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]
        for p in [0, 1]:
            for win in winconditions:
                if np.sum([self.state[9 * p + w] for w in win]) == 3:
                    return True, p
        if np.sum(self.state[0:18]) == 9:
            return True, None
        else:
            return False, None

    def isLegalMove(self, move):
        # returns True if move is legal
        return (self.state[0:9] + self.state[9:18])[move] == 0

    def legalMoves(self):
        # returns list of legal moves
        return [i for i in range(9) if self.isLegalMove(i)]


b = Board()
b.pushMove(8)
b.pushMove(4)
b.popMoves(1)
