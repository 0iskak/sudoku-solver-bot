import math

import keras
import numpy
from PIL.Image import Image as PILImage
from numpy import ndarray

import util
from Image import Image


class Grid:
    images: list[list[ndarray]]
    ints: list[list[int]]
    count = 9
    cell_width: int
    cell_height: int

    def __init__(self, image: PILImage, count=count):
        self.images = []
        self.ints = []

        self.cell_width = cell_width = math.floor(image.width / count)
        self.cell_height = cell_height = math.floor(image.height / count)
        for x in range(count):
            self.images.append([])
            for y in range(count):
                left = x * cell_width
                top = y * cell_height
                cropped = image.crop((
                    left, top,
                    left + cell_width,
                    top + cell_height
                ))

                self.images[x].append(util.preprocess_image_pil(cropped))

    def predict(self, model: keras.Model) -> None:
        for x in range(self.count):
            self.ints.append([])
            for y in range(self.count):
                image = self.images[x][y]
                if image.mean() > 0.98:
                    self.ints[x].append(0)
                    continue

                data = numpy.asarray([image])
                prediction = model.predict(data, verbose=0)
                self.ints[x].append(prediction[0].argmax())
