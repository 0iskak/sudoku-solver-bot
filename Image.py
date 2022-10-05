import math

import PIL.Image
import numpy
from PIL.Image import Image as PILImage
from numpy import ndarray


class Image:
    image: PILImage

    @property
    def width(self):
        return self.image.width

    @property
    def height(self):
        return self.image.height

    def __init__(self, path: str | None):
        if path is None:
            return
        self.image = PIL.Image.open(path).convert('L')

    def padding_crop(self, padding_px=5) -> 'Image':
        self.image = self.image.crop((
            padding_px,
            padding_px,
            self.image.width - padding_px,
            self.image.height - padding_px
        ))

        return self

    def content_crop(self) -> 'Image':
        try:
            left, right = self._content_bounds()
            top, bottom = self._content_bounds(False)

            self.image = self.image.crop((
                left, top,
                right, bottom
            ))
        except TypeError:
            pass

        return self

    def _content_bounds(self, is_x=True) -> tuple[int, int] | None:
        p1 = None
        p2 = None

        v1 = self.height
        v2 = self.width
        if is_x:
            v1, v2 = v2, v1

        def check_pixel(xy: tuple[int, int]) -> int | None:
            if self.image.getpixel(xy) != 255:
                return xy[0 if is_x else 1]
            return None

        for a1 in range(math.floor(v1 / 2)):
            a2 = v1 - a1 - 1

            for b in range(v2):
                if None not in [p1, p2]:
                    break

                c1 = [b, a1]
                c2 = [b, a2]
                if is_x:
                    c1.reverse()
                    c2.reverse()

                if p1 is None:
                    p1 = check_pixel((c1[0], c1[1]))

                if p2 is None:
                    p2 = check_pixel((c2[0], c2[1]))

        try:
            return p1, p2 + 1
        except TypeError:
            return None

    def threshold(self, threshold_lvl=180) -> 'Image':
        self.image = self.image.point(
            lambda point: 255 if point > threshold_lvl else 0
        )
        return self

    def resize(self, width=28, height=28) -> 'Image':
        self.image = self.image.resize((width, height))

        return self

    def save(self, path: str) -> 'Image':
        self.image.save(path)

        return self

    def array(self, flat=False, normalize=True) -> ndarray:
        # noinspection PyTypeChecker
        array = numpy.asarray(self.image)
        if flat:
            array = array.flatten()
        if normalize:
            array = numpy.divide(array, 255)
            array = numpy.around(array, 2)

        return array

    @classmethod
    def from_pil(cls, image: PILImage):
        instance = cls(None)
        instance.image = image.convert('L')

        return instance
