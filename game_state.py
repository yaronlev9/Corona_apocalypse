from enum import Enum
from copy import deepcopy


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
CORONA_ILL_3 = '3'
WALL = '*'
EMPTY_LOCATION = '_'
TARGET = 'W'


class GameState(object):
    def __init__(self, width=WIDTH, height=HEIGHT, corona_1_loc=(7, 2),
                 corona_2_loc=(13, 0), corona_3_loc=(7, 8), location=(0, WIDTH - 1), board=None, mask=False,
                 mask_locations=[(6, 0), (7, 15)]):
        self.__width = width
        self.__height = height
        self.__score = START_SCORE
        self.__corona_1_location = corona_1_loc
        self.__corona_2_location = corona_2_loc
        self.__corona_3_location = corona_3_loc
        self.__mask_locations = mask_locations
        self.__location = location
        self.__board = self.create_board()
        self.__target = (self.__height - 1, 0)
        self.__done = False
        self.__mask = mask
        self.__win = False
        self.dict_of_moves = {Action.UP: False, Action.DOWN: False, Action.RIGHT: False, Action.LEFT: False}
        # self.__first_mask = first_mask

    def create_board(self):
        board = [
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['*', '*', '*', '_', '*', '*', '*', '*', '*', '*', '*', '*', '*', '_', '_', '*'],
            ['*', '_', '_', '_', '*', '*', '*', '*', '*', '*', '*', '*', '*', '_', '_', '*'],
            ['*', '*', '*', '_', '*', '*', '*', '_', '_', '_', '_', '_', '_', '_', '_', '*'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '*', '*', '*', '_', '*', '_', '_', '*'],
            ['_', '*', '*', '_', '_', '*', '*', '*', '*', '_', '_', '_', '*', '_', '_', '*'],
            ['_', '*', '_', '_', '_', '*', '_', '_', '_', '_', '_', '_', '*', '_', '_', '*'],
            ['*', '*', '_', '_', '*', '*', '_', '_', '_', '_', '*', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '*', '_', '_', '*', '*', '*', '*', '*', '*', '_', '*', '*'],
            ['_', '_', '_', '*', '*', '_', '_', '_', '_', '_', '_', '_', '*', '_', '*', '*'],
            ['_', '_', '_', '_', '_', '_', '*', '_', '*', '_', '*', '*', '*', '_', '*', '*'],
            ['*', '*', '*', '_', '*', '_', '*', '_', '*', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '*', '_', '_', '_', '*', '_', '*', '*', '*', '_', '_', '*'],
            ['_', '_', '_', '_', '*', '_', '_', '_', '*', '_', '_', '_', '*', '_', '_', '*'],
            ['_', '*', '_', '*', '*', '_', '*', '_', '*', '*', '*', '*', '*', '_', '*', '*'],
            ['_', '_', '_', '_', '_', '_', '*', '_', '_', '_', '_', '_', '_', '_', '*', '*']]
        if board[self.__corona_1_location[0]][self.__corona_1_location[1]] == '_':
            board[self.__corona_1_location[0]][self.__corona_1_location[1]] = '1'
        if board[self.__corona_2_location[0]][self.__corona_2_location[1]] == '_':
            board[self.__corona_2_location[0]][self.__corona_2_location[1]] = '2'
        if board[self.__corona_3_location[0]][self.__corona_3_location[1]] == '_':
            board[self.__corona_3_location[0]][self.__corona_3_location[1]] = '3'
        board[self.__location[0]][self.__location[1]] = '0'
        for mask in self.__mask_locations:
            if board[mask[0]][mask[1]] == '_':
                board[mask[0]][mask[1]] = 'm'
        return board

    def _is_right_legal_action(self, location, player):
        if location[1] >= self.__width:
            return False
        if player == 0:
            if self.__mask:
                if self.__board[location[0]][location[1]] == '1' or self.__board[location[0]][location[1]] == '2' \
                        or self.__board[location[0]][location[1]] == '3':
                    if location[1] + 1 >= self.__width or self.__board[location[0]][location[1] + 1] != '_':
                        return False
                    self.dict_of_moves[Action.RIGHT] = True
                    return True
                else:
                    if self.__board[location[0]][location[1]] == '_':
                        return True
                    return False
            return self.__board[location[0]][location[1]] == '_' or self.__board[location[0]][location[1]] == 'm'
        return self.__board[location[0]][location[1]] == '_' or (
                self.__board[location[0]][location[1]] == '0' and not self.__mask)

    def _is_left_legal_action(self, location, player):
        if location[1] < 0:
            return False
        if player == 0:
            if self.__mask:
                if self.__board[location[0]][location[1]] == '1' or self.__board[location[0]][location[1]] == '2' \
                        or self.__board[location[0]][location[1]] == '3':
                    if location[1] - 1 < 0 or self.__board[location[0]][location[1] - 1] != '_':
                        return False
                    self.dict_of_moves[Action.LEFT] = True
                    return True
                else:
                    if self.__board[location[0]][location[1]] == '_':
                        return True
                    return False
            return self.__board[location[0]][location[1]] == '_' or self.__board[location[0]][location[1]] == 'm'
        return self.__board[location[0]][location[1]] == '_' or (
                self.__board[location[0]][location[1]] == '0' and not self.__mask)

    def _is_up_legal_action(self, location, player):
        if location[0] < 0:
            return False
        if player == 0:
            if self.__mask:
                if self.__board[location[0]][location[1]] == '1' or self.__board[location[0]][location[1]] == '2' \
                        or self.__board[location[0]][location[1]] == '3':
                    if location[0] - 1 < 0 or self.__board[location[0] - 1][location[1]] != '_':
                        return False
                    self.dict_of_moves[Action.UP] = True
                    return True
                else:
                    if self.__board[location[0]][location[1]] == '_':
                        return True
                    return False
            return self.__board[location[0]][location[1]] == '_' or self.__board[location[0]][location[1]] == 'm'
        return self.__board[location[0]][location[1]] == '_' or (
                self.__board[location[0]][location[1]] == '0' and not self.__mask)

    def _is_down_legal_action(self, location, player):
        if location[0] >= self.__height:
            return False
        if player == 0:
            if self.__mask:
                if self.__board[location[0]][location[1]] == '1' or self.__board[location[0]][location[1]] == '2' \
                        or self.__board[location[0]][location[1]] == '3':
                    if location[0] + 1 >= self.__height or self.__board[location[0] + 1][location[1]] != '_':
                        return False
                    self.dict_of_moves[Action.DOWN] = True
                    return True
                else:
                    if self.__board[location[0]][location[1]] == '_':
                        return True
                    return False
            return self.__board[location[0]][location[1]] == '_' or self.__board[location[0]][location[1]] == 'm'
        return self.__board[location[0]][location[1]] == '_' or (
                self.__board[location[0]][location[1]] == '0' and not self.__mask)

    def get_legal_actions(self, player):
        legal_actions = []
        if player == 0:
            location = self.__location
        elif player == 1:
            location = self.__corona_1_location
        elif player == 2:
            location = self.__corona_2_location
        elif player == 3:
            location = self.__corona_3_location
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
        if action not in self.get_legal_actions(player):
            return
        if player == 0:
            old_location = self.__location
        elif player == 1:
            old_location = self.__corona_1_location
        elif player == 2:
            old_location = self.__corona_2_location
        else:
            old_location = self.__corona_3_location
        if action == Action.UP:
            new_location = (old_location[0] - 1, old_location[1])
            if self.dict_of_moves[Action.UP]:
                new_location = (new_location[0] - 1, new_location[1])
            self.__board[old_location[0]][old_location[1]] = "_"
        elif action == Action.DOWN:
            new_location = (old_location[0] + 1, old_location[1])
            if self.dict_of_moves[Action.DOWN]:
                new_location = (new_location[0] + 1, new_location[1])
            self.__board[old_location[0]][old_location[1]] = "_"
        elif action == Action.RIGHT:
            new_location = (old_location[0], old_location[1] + 1)
            if self.dict_of_moves[Action.RIGHT]:
                new_location = (new_location[0], new_location[1] + 1)
            self.__board[old_location[0]][old_location[1]] = "_"
        elif action == Action.LEFT:
            new_location = (old_location[0], old_location[1] - 1)
            if self.dict_of_moves[Action.LEFT]:
                new_location = (new_location[0], new_location[1] - 1)
            self.__board[old_location[0]][old_location[1]] = "_"
        else:
            new_location = old_location
        if player == 0:
            if action != Action.STOP:
                self.__score -= 1
            self.__location = new_location
            if self.__board[new_location[0]][new_location[1]] == 'm':
                self.__mask = True
                self.__mask_locations.remove(new_location)
                self.__board[new_location[0]][new_location[1]] = EMPTY_LOCATION
            self.__board[new_location[0]][new_location[1]] = '0'
            if new_location == self.__target:
                self.__win = True
                self.__done = True
        elif player == 1:
            self.__corona_1_location = new_location
            if self.__board[new_location[0]][new_location[1]] == '0' and not self.__mask:
                self.__done = True
            self.__board[new_location[0]][new_location[1]] = '1'
        elif player == 2:
            self.__corona_2_location = new_location
            if self.__board[new_location[0]][new_location[1]] == '0' and not self.__mask:
                self.__done = True
            self.__board[new_location[0]][new_location[1]] = '2'
        elif player == 3:
            self.__corona_3_location = new_location
            if self.__board[new_location[0]][new_location[1]] == '0' and not self.__mask:
                self.__done = True
            self.__board[new_location[0]][new_location[1]] = '3'
        for key in self.dict_of_moves:
            self.dict_of_moves[key] = False

    def generate_successor(self, player, action):
        successor = GameState(width=self.__width, height=self.__height,
                              corona_1_loc=self.__corona_1_location,
                              corona_2_loc=self.__corona_2_location,
                              corona_3_loc=self.__corona_3_location,
                              location=self.__location,
                              board=self.__board.copy(), mask=self.__mask, mask_locations=self.__mask_locations)
        successor.apply_action(action, player)
        return successor

    def __str__(self):
        for i in range(self.__height):
            print(self.__board[i])
        return ''

    def get_board(self):
        return self.__board

    def get_target(self):
        return self.__target

    def get_location(self):
        return self.__location

    def get_corona_1_location(self):
        return self.__corona_1_location

    def get_corona_2_location(self):
        return self.__corona_2_location

    def get_corona_3_location(self):
        return self.__corona_3_location

    def get_mask_status(self):
        return self.__mask

    def get_mask_locations(self):
        return self.__mask_locations

    def get_done(self):
        return self.__done

    def get_score(self):
        return self.__score

    def get_win(self):
        return self.__win

    # def get_first_mask(self):
    #     return self.__first_mask
    #
    # def set_first_mask(self, value):
    #     self.__first_mask = value
