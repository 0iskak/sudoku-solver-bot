import numpy
import pynput.mouse
from PIL import ImageGrab
from pynput import keyboard
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
from sudoku import Sudoku

from Grid import Grid
from Model import Model
from Rect import Rect


def mouse_bot(unsolved: Sudoku, solved: Sudoku, cell_size: tuple[int, int]) -> None:
    mouse_controller.position = rect.tl
    mouse_controller.move(-int(cell_size[0] / 2), -int(cell_size[1] / 2))

    size = 9

    for x in range(size):
        mouse_controller.move(cell_size[0], 0)

        for y in range(size):
            mouse_controller.move(0, cell_size[1])

            solved_cell = solved.board[y][x]
            if unsolved.board[y][x] is not None:
                continue
            # noinspection PyTypeChecker
            mouse_controller.click(pynput.mouse.Button.left)
            keyboard_controller.press(str(solved_cell))

        mouse_controller.move(0, cell_size[1] * -size)


def on_press(key) -> None:
    if not isinstance(key, keyboard.KeyCode):
        return

    position = mouse_controller.position
    match key.char:
        case 'q':
            rect.tl = position
            print(f'Top left: {position}')
        case 'w':
            rect.br = position
            print(f'Bottom right: {position}')
        case 'e':
            image = ImageGrab.grab(rect.box)
            print('Screenshot taken')
            grid = Grid(image)
            model = Model.get_model(grid.images[0][0].shape)
            grid.predict(model)

            # noinspection PyTypeChecker
            board: list[list[int]] = numpy \
                .asarray(grid.ints) \
                .transpose().tolist()

            sudoku = Sudoku(3, 3, board)
            print(sudoku)
            print(sudoku.solve())

            mouse_bot(sudoku, sudoku.solve(), (grid.cell_width, grid.cell_height))


if __name__ == '__main__':
    mouse_controller = MouseController()
    keyboard_controller = KeyboardController()
    rect = Rect()

    with keyboard.Listener(on_press=on_press) as key_listener:
        print('Ready')
        key_listener.join()
