from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
import pickle
from tensorflow.keras.models import load_model
import numpy as np


class Evaluator:
    def __init__(self, architecture, loss, optimizer):
        self.architecture = architecture

        self.model = Sequential()
        self.model.add(Dense(architecture[0], input_shape=(18,)))

        for layer in architecture:
            if isinstance(layer, str):
                self.model.add(Activation(layer))
            else:
                self.model.add(Dense(layer))

        self.model.compile(loss=loss, optimizer=optimizer)

    def load_data(self, filename):
        with open(filename, "rb") as f:
            x, y = pickle.load(f)
        self.x_train = np.concatenate(
            list(map(lambda a: a.reshape((1, 18)), x)), axis=0
        )
        self.y_train = np.array(y)

    def load_model(self, filename):
        self.model = load_model(filename)

    def fit(self, epochs=3, batch_size=32):
        self.model.fit(self.x_train, self.y_train, epochs=epochs, batch_size=batch_size)

    def save_model(self):
        model_name = self.filename()
        self.model.save(model_name)
        return model_name

    def evaluate(self, board):
        return self.model.predict(board.reshape((1, 18)))[0][0]

    def name(self):
        return "-".join([str(l) for l in self.architecture])

    def filename(self):
        return self.name() + ".h5"
