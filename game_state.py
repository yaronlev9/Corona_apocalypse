import numpy as np

WIDTH = 16
HEIGHT = 16
START_SCORE = 0
CITIZEN = 1
CORONA_ILL = 2
WALL = 3
EMPTY_LOCATION = '_'


class GameState(object):
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.score = START_SCORE

    def create_board(self):
        board = np.array([[EMPTY_LOCATION, EMPTY_LOCATION],
                          [WALL, WALL, WALL, EMPTY_LOCATION, WALL, WALL, WALL,
                           WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL,
                           WALL, WALL]])
        for i in range(2):
            for j in range(2):
                print(board[i][j])


ga = GameState()
ga.create_board()
