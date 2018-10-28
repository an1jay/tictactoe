from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
import pickle
from tensorflow.keras.models import load_model
import numpy as np

class Evaluator:
    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(64, input_shape=(18, )))
        self.model.add(Activation('tanh'))
        self.model.add(Dense(1))
        self.model.add(Activation('tanh'))
        
        self.model.compile(loss = 'mean_squared_error', optimizer = 'adam')
        
    def load_data(self, filename):
        with open(filename, 'rb') as f:
            x, y = pickle.load(f)
        self.x_train = np.concatenate(list(map(lambda a: a.reshape((1, 18)), x)), axis=0)#.reshape((len(x),18))
        self.y_train = np.array(y)
        
    def load_model(self, filename):
        self.model = load_model(filename)
    
    def fit(self):
        
        self.model.fit(self.x_train, self.y_train, epochs=3)
        
    def save_model(self, model_name):
        self.model.save(model_name)
        
    def evaluate(self, board):
        return self.model.predict(board.reshape((1,18)))[0][0]