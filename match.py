import math
import numpy as np
from game import TicTacToe
from progress import progress


class Match:
    def __init__(self, p1, p2, verbose):
        self.p1 = p1
        self.p2 = p2
        self.VERBOSE = verbose
        # self.t = TicTacToe(p1, p2, verbose=self.VERBOSE)
        
    def play(self, numGames):
        score = np.zeros((2, 3))

        def playHalf(p1, p2, numG, games):
            t = TicTacToe(p1, p2, verbose=self.VERBOSE)
            result = np.zeros(3)
            for g in range(numG):
                if g % math.ceil(0.05 * numGames) == 0:
                    progress(games + g, numGames, status="Playing Games")
                print()
                winner = t.play()
                t.reset()
                result[winner + 1] += 1
            return result

        score[0] = np.flip(playHalf(self.p1, self.p2, numGames // 2, 0), 0)
        score[1] = playHalf(self.p2, self.p1, numGames // 2, numGames // 2)
        return score
