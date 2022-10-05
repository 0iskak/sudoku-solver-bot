import logging
import os

from numpy import ndarray

from Image import Image
from PIL.Image import Image as PILImage


def preprocess_image_path(digit_path: str) -> ndarray:
    return preprocess_image(Image(digit_path))


def preprocess_image_pil(image: PILImage) -> ndarray:
    return preprocess_image(Image.from_pil(image))


def preprocess_image(image: Image) -> ndarray:
    return image \
        .padding_crop() \
        .threshold() \
        .content_crop() \
        .resize() \
        .array()


def get_digits(path: str) -> tuple[list[ndarray], list[int]]:
    data: list[ndarray] = []
    labels: list[int] = []

    for i in range(10):
        logging.info(f'Preprocessing {i}')

        digits_path = os.path.join(path, str(i))

        digits = list(map(
            lambda digit_path: preprocess_image_path(os.path.join(digits_path, digit_path)),
            os.listdir(digits_path)
        ))
        data.extend(digits)
        labels.extend([i] * len(digits))

    return data, labels
