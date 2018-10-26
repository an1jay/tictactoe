# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 16:41:40 2018

@author: Anirudh
"""
import numpy as np
import os
import pickle
import random
import sys
import time
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils import plot_model

from game import TicTacToe


BLANK = ' '
EXIT = '-'

def smartPrint(statement, verbose, last='\n'):
    # =========================================================================
    # Utility method to print statement if verbose = True
    # =========================================================================
    if verbose:
        print(statement, end=last)
    else:
        pass


class Player:
    def __init__(self):
        pass

    def startGame(self):
        # =====================================================================
        # Do set up in this method
        # =====================================================================
        pass

    def move(self, board):
        # =====================================================================
        # Make move given the state of the board
        # =====================================================================
        pass

    def reward(self, *args):
        # =====================================================================
        # Only for Q Learning Player - reward the player so the Q Learning
        # Player can update the Q value
        # =====================================================================
        pass

    def printBoard(self, board):
        # =====================================================================
        # Utility Method to print the board to console
        # =====================================================================
        print('|'.join(board[0:3]))
        print('|'.join(board[3:6]))
        print('|'.join(board[6:9]))


class HumanPlayer(Player):
    def __init__(self, verbose=True):
        self.VERBOSE = verbose

    def startGame(self):
        # =====================================================================
        # Tell player it is the start of a new game
        # =====================================================================
        smartPrint('============', verbose=self.VERBOSE)
        smartPrint('New Game', verbose=self.VERBOSE)
        smartPrint('============', verbose=self.VERBOSE)

    def move(self, board):
        # =====================================================================
        # Get move from player by showing board
        # =====================================================================
        while True:
            try:
                self.printBoard(board)
                move = input('Your move? (1-9 or - to exit)\n')
                print('============')
                if (move == EXIT):
                    sys.exit(0)
                move = int(move)
                if not (move-1 in range(9)):
                    raise ValueError
            except ValueError:
                print('Invalid move; try again:\n')
            else:
                return move-1


class QLearnerPlayer(Player):
    def __init__(self, verbose=False, epsilon=0.4, alpha=0.3, gamma=0.9, defaultQ = 1):
        self.VERBOSE = verbose
        self.EPSILON = epsilon  # chance of random exploration
        self.ALPHA = alpha  # discount factor for future reward
        self.GAMMA = gamma  # learning rate
        self.DEFAULTQ = defaultQ  # default q-value for new state, action pairs
        # Generate neural network

        self.q = Sequential()
        self.q.add(Dense(64, activation='tanh', input_dim=36))
        #self.q.add(Dense(64, activation='relu'))
        self.q.add(Dense(9))
        self.q.compile(optimizer='adam', loss='mean_squared_error')
        # plot_model(self.q, to_file='model.png')
        # print('NAME', self.q.get_layer(index=4).output_shape)
        self.prevMove = None  # Previous move
        self.prevBoard = (' ',) * 9

    def availableMoves(self, board):
        # =====================================================================
        # Get all legal moves in the board
        # =====================================================================
        return [i for i in range(9) if board[i] == ' ']

    def startGame(self):
        pass

    def getQ(self, state, action):
        # =====================================================================
        # Get Q-Value for (State, Action) pair. If no Q-Value exists for a
        # (State, Action) pair, create Q-Value of DEFAULTQ for that pair
        # =====================================================================
        return self.q.predict([self.vectoriseSA(state, action)], batch_size=1)

    def move(self, board):
        # =====================================================================
        # Get move by picking randomly (with probability epsilon) and otherwise
        # picking the (one of the) action(s) with the highest Q-Value, given
        # the current state (i.e. board), or if
        # =====================================================================
        self.prevBoard = tuple(board)
        actions = self.availableMoves(board)
        # Choose random action with epsilon chance
        if random.random() < self.EPSILON:
            self.prevMove = random.choice(actions)
            return self.prevMove
        # Otherwise choose action(s) with highest Q value
        QValues = [self.getQ(self.prevBoard, a) for a in actions]
        #print(QValues)
        maxQValue = max(QValues)
        # If multiple best actions, choose one at random
        if QValues.count(maxQValue) > 1:
            bestActions = [i for i in range(len(actions)) if QValues[i] == maxQValue]
            bestMove = actions[random.choice(bestActions)]
        # If only one best action, choose that
        else:
            bestMove = actions[QValues.index(maxQValue)]
        self.prevMove = bestMove
        return self.prevMove

    def reward(self, value, board):
        # =====================================================================
        # Update Q value for the (State, Action) pair just played in the 'move'
        # method
        # =====================================================================
        if self.prevMove:
            prevQ = self.getQ(self.prevBoard, self.prevMove)
            maxQnew = max([self.getQ(tuple(board), a) for a in self.availableMoves(self.prevBoard)])

            self.q.fit(self.vectoriseSA(self.prevBoard, self.prevMove),
                       prevQ + self.ALPHA *((value + self.GAMMA * maxQnew)-prevQ),
                       #batch_size=1,
                       epochs = 3, verbose=0)
        # Clear previous move and previous board variables
        self.prevBoard = None
        self.prevMove = None

    def vectoriseSA(self, board, action):
        # =====================================================================
        # Vectorise (State, Action) pair in a 'one-hot' manner
        # =====================================================================
        vector = []
        u_board = ['O', ' ', 'X']
        for b in board:
            for b_u in u_board:
                if b == b_u:
                    vector.append(1)
                else:
                    vector.append(0)
        for a in range(9):
            if action == a:
                vector.append(1)
            else:
                vector.append(0)
        output = np.array([vector])
        return output

if __name__ == '__main__':
    trainCycles = 50000
    trainEpsilon = 0.4
    p1 = QLearnerPlayer()
    p2 = QLearnerPlayer()

    print('Training')
    p1.EPSILON = trainEpsilon
    p2.EPSILON = trainEpsilon
    
    t0 = time.time()
    
    for i in range(trainCycles):
        if i % 50 == 0:
            print('{0:.1f}%, '.format(i*100/trainCycles) + str(int(time.time()-t0)) + 's',  end = ' |\n')
            #print('{0:.2f}%'.format(i*100/20000), end = ' | ')
        t = TicTacToe(p1, p2)
        t.play()

    #pickle.dump((p1, p2), open('nnAI.pkl', 'wb'))
    print('\nTraining Done')

    p1.EPSILON = 0
    p2 = HumanPlayer()
    j = TicTacToe(p1, p2, verbose=True)
    j.play()
