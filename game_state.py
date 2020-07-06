from enum import Enum


class Action(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    STOP = "STOP"


WIDTH = 16
HEIGHT = 16
START_SCORE = 0
CITIZEN = '0'
CORONA_ILL_1 = '1'
CORONA_ILL_2 = '2'
WALL = '-'
EMPTY_LOCATION = '_'
TARGET = 'W'


def create_board():
    board = [
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '0'],
        ['-', '-', '-', '_', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '_', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '_', '-', '-', '-', '_', '_', '_', '_', '_', '-', '-', '-', '-'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '-', '-', '-', '_', '-', '-', '-', '-'],
        ['_', '-', '-', '_', '-', '-', '-', '-', '-', '_', '-', '_', '-', '-', '-', '-'],
        ['_', '-', '_', '_', '-', '1', '_', '_', '_', '_', '-', '_', '-', '-', '-', '-'],
        ['-', '-', '_', '-', '-', '_', '_', '_', '_', '_', '-', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '-', '_', '_', '-', '-', '-', '-', '-', '-', '-', '_', '-', '-'],
        ['_', '-', '-', '-', '-', '_', '_', '_', '_', '_', '_', '_', '-', '_', '-', '-'],
        ['_', '_', '_', '_', '_', '_', '-', '_', '-', '_', '-', '-', '-', '_', '-', '-'],
        ['-', '-', '-', '_', '-', '_', '-', '_', '-', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '-', '_', '-', '_', '-', '_', '-', '-', '-', '_', '-', '-'],
        ['2', '_', '_', '_', '-', '_', '-', '_', '-', '_', '_', '_', '-', '_', '-', '-'],
        ['_', '-', '-', '-', '-', '_', '-', '_', '-', '-', '-', '-', '-', '_', '-', '-'],
        ['W', '_', '_', '_', '_', '_', '-', '_', '_', '_', '_', '_', '_', '_', '-', '-']]

    return board


class GameState(object):
    def __init__(self, width=WIDTH, height=HEIGHT, corona_1_loc=(6, 5),
                 corona_2_loc=(13, 0), location=(0, WIDTH - 1), board=None):
        self.__width = width
        self.__height = height
        self.__score = START_SCORE
        self.__board = create_board()
        self.__location = location
        self.__corona_1_location = corona_1_loc
        self.__corona_2_location = corona_2_loc
        self.__target = (self.__height - 1, 0)
        self.__done = False
        self.__mask = False

    def _is_right_legal_action(self, location, player):
        if location[1] >= self.__width:
            return False
        if player == 0:
            if self.__mask:
                if self.__board[location[0]][location[1]] == '-':
                    return False
                return True
            return self.__board[location[0]][location[1]] == '_' or \
                   self.__board[location[0]][location[1]] == 'm'
        return self.__board[location[0]][location[1]] == '_'

    def _is_left_legal_action(self, location, player):
        if location[1] < 0:
            return False
        if player == 0:
            if self.__mask:
                if self.__board[location[0]][location[1]] == '-':
                    return False
                return True
            return self.__board[location[0]][location[1]] == '_' or \
                   self.__board[location[0]][location[1]] == 'm'
        return self.__board[location[0]][location[1]] == '_'

    def _is_up_legal_action(self, location, player):
        if location[0] < 0:
            return False
        if player == 0:
            if self.__mask:
                if self.__board[location[0]][location[1]] == '-':
                    return False
                return True
            return self.__board[location[0]][location[1]] == '_' or \
                   self.__board[location[0]][location[1]] == 'm'
        return self.__board[location[0]][location[1]] == '_'

    def _is_down_legal_action(self, location, player):
        if location[0] >= self.__height:
            return False
        if player == 0:
            if self.__mask:
                if self.__board[location[0]][location[1]] == '-':
                    return False
                return True
            return self.__board[location[0]][location[1]] == '_' or \
                   self.__board[location[0]][location[1]] == 'm'
        return self.__board[location[0]][location[1]] == '_'

    def get_legal_actions(self, player):
        legal_actions = []
        if player == 0:
            location = self.__location
        elif player == 1:
            location = self.__corona_1_location
        elif player == 2:
            location = self.__corona_2_location
        else:
            raise Exception("Illegal agent index.")
        if self._is_right_legal_action((location[0], location[1] + 1), player):
            legal_actions.append(Action.RIGHT)
        if self._is_left_legal_action((location[0], location[1] - 1), player):
            legal_actions.append(Action.LEFT)
        if self._is_up_legal_action((location[0] - 1, location[1]), player):
            legal_actions.append(Action.UP)
        if self._is_down_legal_action((location[0] + 1, location[1]), player):
            legal_actions.append(Action.DOWN)
        legal_actions.append(Action.STOP)
        return legal_actions

    def apply_action(self, action, player):
        # if action not in self.get_legal_actions(player):
        #     raise Exception("illegal action.")
        if player == 0:
            old_location = self.__location
        elif player == 1:
            old_location = self.__corona_1_location
        else:
            old_location = self.__corona_2_location
        if action == Action.UP:
            new_location = (old_location[0] - 1, old_location[1])
            self.__board[old_location[0]][old_location[1]] = "_"
        elif action == Action.DOWN:
            new_location = (old_location[0] + 1, old_location[1])
            self.__board[old_location[0]][old_location[1]] = "_"
        elif action == Action.RIGHT:
            new_location = (old_location[0], old_location[1] + 1)
            self.__board[old_location[0]][old_location[1]] = "_"
        elif action == Action.LEFT:
            new_location = (old_location[0], old_location[1] - 1)
            self.__board[old_location[0]][old_location[1]] = "_"
        else:
            new_location = old_location
        if player == 0:
            self.__location = new_location
            if self.__board[new_location[0]][new_location[1]] == 'm':
                self.__mask = True
            self.__board[new_location[0]][new_location[1]] = '0'
        elif player == 1:
            self.__corona_1_location = new_location
            self.__board[new_location[0]][new_location[1]] = '1'
        elif player == 2:
            self.__corona_2_location = new_location
            self.__board[new_location[0]][new_location[1]] = '2'

    def generate_successor(self, player, action):
        successor = GameState(width=self.__width, height=self.__height,
                              corona_1_loc=self.__corona_1_location,
                              corona_2_loc=self.__corona_2_location,
                              location=self.__location,
                              board=self.__board.copy())
        successor.apply_action(action, player)
        return successor

    def __str__(self):
        for i in range(self.__height):
            print(self.__board[i])
        return ''


ga = GameState()
print(ga)
print(ga)
t = ga.generate_successor(0, Action.LEFT)
print(t)
