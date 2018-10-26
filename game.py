import random

def smartPrint(statement, verbose, last='\n'):
    # =========================================================================
    # Utility method to print statement if verbose = True
    # =========================================================================
    if verbose:
        print(statement, end=last)
    else:
        pass


class TicTacToe:
    def __init__(self, player1, player2, verbose=False):
        self.VERBOSE = verbose
        self.P1CHAR = 'X'
        self.P2CHAR = 'O'

        self.player1 = player1
        self.player2 = player2

        self.player1turn = random.choice([True, False])
        self.board = [' '] * 9

    def play(self):
        # =====================================================================
        # Main method of the class - actually plays the game
        # =====================================================================

        # Initialise players
        self.player1.startGame()
        self.player2.startGame()

        # Main game loop
        while True:
            if self.player1turn:
                player = self.player1
                otherplayer = self.player2
                chars = (self.P1CHAR, self.P2CHAR)
            else:
                player = self.player2
                otherplayer = self.player1
                chars = (self.P2CHAR, self.P1CHAR)
            # Player moves
            move = player.move(self.board)
            # If illegal move is made, reward player -99 and exit game
            if self.board[move] != ' ':
                player.reward(-99, self.board[:])
                print('Illegal move!!')
                break
            self.board[move] = chars[0]
            # Check winner
            gameOver, whoWon = self.isGameOver(chars)
            # If game over, reward winner 1 and loser, -1; if tie, reward both 0.5 and break from loop
            # If not game over reward player 0
            if gameOver:
                if whoWon == chars[0]:
                    if self.VERBOSE:
                        player.printBoard(self.board[:])
                    smartPrint('\n %s won!' % player.__class__.__name__, verbose=self.VERBOSE)
                    player.reward(1, self.board[:])
                    otherplayer.reward(-1, self.board[:])
                if whoWon == chars[1]:
                    if self.VERBOSE:
                        player.printBoard(self.board[:])
                    smartPrint('\n %s won!' % otherplayer.__class__.__name__, verbose=self.VERBOSE)
                    otherplayer.reward(1, self.board[:])
                    player.reward(-1, self.board[:])
                else:
                    if self.VERBOSE:
                        player.printBoard(self.board[:])
                    smartPrint('Tie!', verbose=self.VERBOSE)
                    player.reward(0.5, self.board[:])
                    otherplayer.reward(0.5, self.board[:])
                break
            else:
                player.reward(0, self.board[:])
            self.player1turn = not self.player1turn

    def isGameOver(self, chars):
        # =====================================================================
        # Returns (gameOver, char), where gameOver is a Boolean indicating
        # whether the game is over and char is the character of the winning
        # player. If char is None, no winner.
        # =====================================================================
        top = self.board[0:3]
        mid = self.board[3:6]
        bot = self.board[6:9]
        for char in chars:
            # check horizontal victories
            for j in range(3):
                gameOver = top[j] == char and mid[j] == char and bot[j] == char
                if gameOver:
                    return (gameOver, char)
            # check vertical victories
            for row in [top, mid, bot]:
                gameOver = row[0] == char and row[1] == char and row[2] == char
                if gameOver:
                    return (gameOver, char)

            # check diagonal victories
            gameOver = top[0] == char and mid[1] == char and bot[2] == char
            if gameOver:
                return (gameOver, char)
            gameOver = top[2] == char and mid[1] == char and bot[0] == char
            if gameOver:
                return (gameOver, char)

        # check for draw - 0 spaces left
        if (self.board.count(' ') == 0):
            return (True, None)
        else:
            return (False, None)

