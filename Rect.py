class Rect:
    tl: tuple[int, int]
    br: tuple[int, int]

    @property
    def box(self) -> tuple[int, int, int, int]:
        return (
            self.tl[0],
            self.tl[1],
            self.br[0],
            self.br[1]
        )
