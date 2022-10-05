import logging

import numpy

import util
from Model import Model

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

data, labels = util.get_digits('C:\\Users\\Iskak\\Downloads\\digits')

data = numpy.asarray(data)
labels = numpy.asarray(labels)
model = Model(data[0].shape)
model.load()

model.fit(data, labels, 16, 100, 1)
Model.save_model(model)
