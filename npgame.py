import numpy as np

class TicTacToe:
    def __init__(self, player1, player2, rewards, verbose):
        self.players = [player1,player2]
        
        self.REWARDS = rewards # tuple (win, loss, draw, inbetweenmove) make named tuple
        self.VERBOSE = verbose

        self.board = np.zeros((2,9)) # 1st row is player 1, 2nd row is player 2
    
    def isLegalMove(self,move): # call before making a move
        return (self.board[0]+self.board[1])[move]==0
        
    def play(self):
        for player in self.players:
            player.startGame()
        
        for p in range(len(self.players)):
            move = self.players[p].move()
            
            if not self.isLegalMove(move):
                self.players[p].reward(self.REWARDS[1])
                break
                
            else:
                self.board[p,move] = 1
            
            isover, winner =  self.isGameOver()
            
            if isover and (not winner is None):
                self.players[winner].reward(self.REWARDS[0])
                self.players[1-winner].reward(self.REWARDS[1])
            
            elif winner is None:
                for player in self.players:
                    player.reward(self.REWARDS[2])
                    
            else:
                self.players[p].reward(self.REWARDS[3])
                    
                            
                
    def isGameOver(self):
        winconditions = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for p in range(len(self.players)):
            for win in winconditions:
                if np.sum([self.board[p,w] for w in win])==3:
                    return True , p
        if np.sum(self.board)==9:
            return True , None
        return False, None


