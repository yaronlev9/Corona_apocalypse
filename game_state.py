import numpy as np

WIDTH = 16
HEIGHT = 16
START_SCORE = 0
CITIZEN = 1
CORONA_ILL = 2
WALL = '-'
EMPTY_LOCATION = '_'
TARGET = 'W'


def create_board():
    board = np.array([['_______________' + '1'], ['---_' + '-' * 12],
                      ['---_' + '-' * 12], ['---_---_____----'],
                      ['________---_----'], ['_--_-----_-_----'],
                      ['_-__-_____-_----'], ['--_--_____-_____'],
                      ['___-__-------_--'], ['_----_______-_--'],
                      ['______-_-_---_--'], ['---_-_-_-_______'],
                      ['____-_-_-_---_--'], ['____-_-_-___-_--'],
                      ['_----_-_-----_--'], ['W_____-_______--']])
    return board


class GameState(object):
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.score = START_SCORE
        self.board = create_board()


ga = GameState()
create_board()
