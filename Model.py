import keras
from keras import Sequential
from keras.layers import Input, Conv1D, MaxPooling1D, Flatten, Dense
from keras.optimizers import SGD


class Model(Sequential):
    path = 'model'

    def __init__(self, shape: tuple):
        super().__init__([
            Input(shape),
            Conv1D(32, 3, activation='relu', kernel_initializer='he_uniform'),
            MaxPooling1D(),
            Conv1D(64, 3, activation='relu', kernel_initializer='he_uniform'),
            Conv1D(64, 3, activation='relu', kernel_initializer='he_uniform'),
            MaxPooling1D(),
            Flatten(),
            Dense(100, activation='relu', kernel_initializer='he_uniform'),
            Dense(10, activation='softmax')
        ])

        self.compile(
            SGD(momentum=0.9),
            'sparse_categorical_crossentropy',
            ['accuracy']
        )

    def load(self) -> 'Model':
        # noinspection PyBroadException
        try:
            self.load_weights(self.path)
        except:
            pass

        return self

    @classmethod
    def save_model(cls, model: keras.Model) -> None:
        model.save_weights(cls.path)

    @classmethod
    def get_model(cls, shape: tuple) -> 'Model':
        model = cls(shape)
        model.load_weights(model.path)

        return model
