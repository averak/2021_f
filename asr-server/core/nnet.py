import os
from tensorflow.keras import layers
from tensorflow.keras import Sequential
import numpy as np

from core import config


class NNet:
    def __init__(self):
        self.nnet: Sequential = self.make_nnet()

    def make_nnet(self) -> Sequential:
        result: Sequential = Sequential()
        result.add(layers.Input(shape=config.INPUT_SHAPE))
        result.add(layers.Conv2D(32, (3, 3), activation='relu'))
        result.add(layers.MaxPool2D((2, 2)))
        result.add(layers.Conv2D(64, (3, 3), activation='relu'))
        result.add(layers.MaxPool2D((2, 2)))
        result.add(layers.Conv2D(64, (3, 3), activation='relu'))

        result.add(layers.Flatten())
        result.add(layers.Dense(64, activation='relu'))
        result.add(layers.Dense(config.N_CLASSES, activation='softmax'))

        # result.summary()

        # make & compile
        result.compile(
            optimizer=config.OPTIMIZER,
            loss=config.LOSS,
            metrics=config.METRICS,
        )

        # load trained weights
        if os.path.exists(config.MODEL_PATH):
            result.load_weights(config.MODEL_PATH)

        return result

    def train(self, x: np.ndarray, y: np.ndarray) -> None:
        for step in range(config.EPOCHS):
            self.nnet.fit(
                x,
                y,
                initial_epoch=step,
                epochs=step + 1,
                batch_size=config.BATCH_SIZE,
                validation_split=config.VALIDATION_SPLIT,
            )

            # save checkpoint
            self.nnet.save_weights('%s/%d.h5' % (config.MODEL_ROOT_PATH, step))

        # save final weights
        self.nnet.save_weights(config.MODEL_PATH)

    def predict(self, vector: np.ndarray) -> int:
        result: int = np.argmax(self.nnet.predict(vector))[0]
        return result
