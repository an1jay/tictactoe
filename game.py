import collections
import numpy as np

Reward = collections.namedtuple("Reward", ["win", "loss", "tie", "endofmove"])


class TicTacToe:
    def __init__(
        self,
        player1,
        player2,
        verbose,
        rewards=(1, -1, 0.5, 0),
        recordGame=False,
    ):
        self.players = [player1, player2]
        self.REWARDS = Reward(*rewards)
        # tuple (win, loss, draw, inbetweenmove)
        # make named tuple
        self.RECORDGAME = recordGame
        self.VERBOSE = verbose
        self.board = np.zeros(
            (2, 9)
        )  # 1st row is player 1, 2nd row is player 2
        if self.RECORDGAME:
            self.gameHistory = [np.array(self.board[:])]

    def isLegalMove(self, move):
        # call before making a move
        return (self.board[0] + self.board[1])[move] == 0

    def play(self):
        # returns 1 in p1 wins, -1 if p2 wins, 0 if tie
        for player in self.players:
            player.startGame()

        self.smartPrint(
            "Match between "
            + self.players[0].__class__.__name__
            + " (player 1, 'X') and "
            + self.players[1].__class__.__name__
            + " (player 2, 'O')."
        )
        gameGoing = True
        while gameGoing:
            if self.VERBOSE:
                self.boardPrint()
            for p in range(len(self.players)):
                move = self.players[p].move(self.board)
                self.smartPrint(
                    self.players[p].__class__.__name__ + " played " + str(move)
                )
                if not self.isLegalMove(move):
                    self.players[p].reward(self.REWARDS.loss)
                    gameGoing = False
                    self.smartPrint("Illegal move!\n")
                    if self.VERBOSE:
                        self.boardPrint()
                    return 1 - 2 * p
                else:
                    self.board[p, move] = 1
                    if self.RECORDGAME:
                        self.gameHistory.append(np.array(self.board[:]))
                isover, winner = self.isGameOver()
                if isover and (not winner is None):
                    self.players[winner].reward(self.REWARDS.win)
                    self.players[1 - winner].reward(self.REWARDS.loss)
                    gameGoing = False
                    self.smartPrint(
                        self.players[winner].__class__.__name__
                        + " (player "
                        + str(winner + 1)
                        + ", "
                        + ["X", "O"][winner]
                        + ") won!"
                    )
                    if self.VERBOSE:
                        self.boardPrint()
                    return 1 - 2 * winner
                elif isover and winner is None:
                    self.players[0].reward(self.REWARDS.tie)
                    self.players[1].reward(self.REWARDS.tie)
                    gameGoing = False
                    self.smartPrint("Tie!")
                    if self.VERBOSE:
                        self.boardPrint()
                    return 0
                else:
                    self.players[p].reward(self.REWARDS.endofmove)

    def isGameOver(self):
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
        for p in range(len(self.players)):
            for win in winconditions:
                if np.sum([self.board[p, w] for w in win]) == 3:
                    return True, p
        if np.sum(self.board) == 9:
            return True, None
        else:
            return False, None

    def smartPrint(self, x, ending="\n"):
        if self.VERBOSE:
            print(x, end=ending)

    def boardPrint(self, msg=""):
        print(msg)
        strbrd = []
        for x, o in zip(self.board[0], self.board[1]):
            if x:
                char = "X"
            elif o:
                char = "O"
            else:
                char = " "
            strbrd.append(char)
        print("|".join(strbrd[:3]))
        print("|".join(strbrd[3:6]))
        print("|".join(strbrd[6:]))
