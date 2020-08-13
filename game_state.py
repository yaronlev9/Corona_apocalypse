from enum import Enum
from copy import deepcopy


class Action(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    STOP = "STOP"


START_SCORE = 0
CITIZEN = '0'
WALL = '*'
EMPTY_LOCATION = '_'
TARGET = 'W'


class GameState(object):
    """
    a class that holds all the attributes of a state in the game.
    """
    def __init__(self, target, mask_locations, coronas, width, height, location, board=None, mask=False,
                 first_mask=True):
        self.__width = width
        self.__height = height
        self.__score = START_SCORE
        self.__coronas = coronas
        self.__mask_locations = mask_locations
        self.__location = location
        self.__target = target
        self.__board = self.create_board(board)
        self.__done = False
        self.__mask = mask
        self.__win = False
        self.dict_of_moves = {Action.UP: False, Action.DOWN: False, Action.RIGHT: False, Action.LEFT: False}
        self.__first_mask = first_mask

    def create_board(self, draft_board):
        """
        creates a new boards matrix, with given attributes from the constructor.
        """
        board = draft_board
        counter = 1
        board[self.__location[0]][self.__location[1]] = '0'
        if board[self.__target[0]][self.__target[1]] == '_':
            board[self.__target[0]][self.__target[1]] = 't'
        for mask in self.__mask_locations:
            if board[mask[0]][mask[1]] == '_':
                board[mask[0]][mask[1]] = 'm'
        for corona in self.__coronas:
            if board[corona[0]][corona[1]] == '_':
                board[corona[0]][corona[1]] = str(counter)
                counter += 1
        return board

    def _is_right_legal_action(self, location, player):
        """
        checks if a move to the right is legal considering the board state for a given player.
        """
        if location[1] >= self.__width:
            return False
        if player == 0:
            if self.__mask:
                flag = False
                for corona in self.__coronas:
                    if location == corona:
                        flag = True
                if flag:
                    if location[1] + 1 >= self.__width or self.__board[location[0]][location[1] + 1] != '_':
                        return False
                    self.dict_of_moves[Action.RIGHT] = True
                    return True
                else:
                    if self.__board[location[0]][location[1]] == '_' or self.__board[location[0]][location[1]] == 'm' \
                            or self.__board[location[0]][location[1]] == 't':
                        return True
                    return False
            return self.__board[location[0]][location[1]] == '_' or self.__board[location[0]][location[1]] == 'm' or \
                   self.__board[location[0]][location[1]] == 't'
        return self.__board[location[0]][location[1]] == '_' or (self.__board[location[0]][location[1]] == '0'
                                                                 and not self.__mask) or \
               self.__board[location[0]][location[1]] == 't'

    def _is_left_legal_action(self, location, player):
        """
        checks if a move to the left is legal considering the board state for a given player.
        """
        if location[1] < 0:
            return False
        if player == 0:
            if self.__mask:
                flag = False
                for corona in self.__coronas:
                    if location == corona:
                        flag = True
                if flag:
                    if location[1] - 1 < 0 or self.__board[location[0]][location[1] - 1] != '_':
                        return False
                    self.dict_of_moves[Action.LEFT] = True
                    return True
                else:
                    if self.__board[location[0]][location[1]] == '_' or self.__board[location[0]][location[1]] == 'm' \
                            or self.__board[location[0]][location[1]] == 't':
                        return True
                    return False
            return self.__board[location[0]][location[1]] == '_' or self.__board[location[0]][location[1]] == 'm' or \
                   self.__board[location[0]][location[1]] == 't'
        return self.__board[location[0]][location[1]] == '_' or (
                self.__board[location[0]][location[1]] == '0' and not self.__mask) or \
               self.__board[location[0]][location[1]] == 't'

    def _is_up_legal_action(self, location, player):
        """
        checks if up move is legal considering the board state for a given player.
        """
        if location[0] < 0:
            return False
        if player == 0:
            if self.__mask:
                flag = False
                for corona in self.__coronas:
                    if location == corona:
                        flag = True
                if flag:
                    if location[0] - 1 < 0 or self.__board[location[0] - 1][location[1]] != '_':
                        return False
                    self.dict_of_moves[Action.UP] = True
                    return True
                else:
                    if self.__board[location[0]][location[1]] == '_' or self.__board[location[0]][location[1]] == 'm' \
                            or self.__board[location[0]][location[1]] == 't':
                        return True
                    return False
            return self.__board[location[0]][location[1]] == '_' or self.__board[location[0]][location[1]] == 'm' or \
                   self.__board[location[0]][location[1]] == 't'
        return self.__board[location[0]][location[1]] == '_' or (
                self.__board[location[0]][location[1]] == '0' and not self.__mask) or \
               self.__board[location[0]][location[1]] == 't'

    def _is_down_legal_action(self, location, player):
        """
        checks if down move is legal considering the board state for a given player.
        """
        if location[0] >= self.__height:
            return False
        if player == 0:
            if self.__mask:
                flag = False
                for corona in self.__coronas:
                    if location == corona:
                        flag = True
                if flag:
                    if location[0] + 1 >= self.__height or self.__board[location[0] + 1][location[1]] != '_':
                        return False
                    self.dict_of_moves[Action.DOWN] = True
                    return True
                else:
                    if self.__board[location[0]][location[1]] == '_' or self.__board[location[0]][location[1]] == 'm' \
                            or self.__board[location[0]][location[1]] == 't':
                        return True
                    return False
            return self.__board[location[0]][location[1]] == '_' or self.__board[location[0]][location[1]] == 'm' or \
                   self.__board[location[0]][location[1]] == 't'
        return self.__board[location[0]][location[1]] == '_' or (
                self.__board[location[0]][location[1]] == '0' and not self.__mask) or \
               self.__board[location[0]][location[1]] == 't'

    def get_legal_actions(self, player):
        """
        gets all of the legal actions for a given player.
        """
        legal_actions = []
        if player == 0:
            location = self.__location
        else:
            location = self.__coronas[player - 1]
        if self._is_right_legal_action((location[0], location[1] + 1), player):
            legal_actions.append(Action.RIGHT)
        if self._is_left_legal_action((location[0], location[1] - 1), player):
            legal_actions.append(Action.LEFT)
        if self._is_up_legal_action((location[0] - 1, location[1]), player):
            legal_actions.append(Action.UP)
        if self._is_down_legal_action((location[0] + 1, location[1]), player):
            legal_actions.append(Action.DOWN)
        if len(legal_actions) == 0:
            legal_actions.append(Action.STOP)
        return legal_actions

    def apply_action(self, action, player):
        """
        applies a given action on the game board, for a given player.
        """
        if action not in self.get_legal_actions(player):
            return
        if player == 0:
            old_location = self.__location
        else:
            old_location = self.__coronas[player - 1]
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
                self.__score += 1
            self.__location = new_location
            if self.__board[new_location[0]][new_location[1]] == 'm' and new_location in self.__mask_locations:
                self.__mask = True
                # self.__mask_locations.remove(new_location)
                self.__board[new_location[0]][new_location[1]] = EMPTY_LOCATION
            self.__board[new_location[0]][new_location[1]] = '0'
            if new_location == self.__target:
                self.__win = True
                self.__done = True
        else:
            self.__coronas[player - 1] = new_location
            if self.__board[new_location[0]][new_location[1]] == '0' and not self.__mask:
                self.__done = True
            self.__board[new_location[0]][new_location[1]] = str(player)
            if old_location == self.__target and old_location != new_location:
                self.__board[old_location[0]][old_location[1]] = 't'
        for key in self.dict_of_moves:
            self.dict_of_moves[key] = False

    def generate_successor(self, player, action):
        """
        generates a successor for a game state with a given action.
        """
        successor = GameState(target=self.__target,
                              mask_locations=deepcopy(self.__mask_locations),
                              coronas=deepcopy(self.__coronas),
                              width=self.__width,
                              height=self.__height,
                              location=self.__location,
                              board=deepcopy(self.__board),
                              mask=self.__mask,
                              first_mask=self.__first_mask)
        successor.apply_action(action, player)
        return successor

    def __str__(self):
        """
        used to print a board.
        """
        for i in range(self.__height):
            print(self.__board[i])
        return ''

    def get_board(self):
        """
        gets the current board.
        """
        return self.__board

    def get_target(self):
        """
        gets the location of the target.
        """
        return self.__target

    def get_location(self):
        """
        gets the current location of the player.
        """
        return self.__location

    def get_mask_status(self):
        """
        returns true iff the player has a mask on.
        """
        return self.__mask

    def get_mask_locations(self):
        """
        gets the list of all the mask locations on the board.
        """
        return self.__mask_locations

    def get_done(self):
        """
        returns true iff the game has got to an end.
        """
        return self.__done

    def get_score(self):
        """
        gets the score of the player.
        """
        return self.__score

    def get_win(self):
        """
        returns true iff the player has won.
        """
        return self.__win

    def get_first_mask(self):
        """
        returns true iff the player did not take a mask yet.
        """
        return self.__first_mask

    def get_width(self):
        """
        returns the width of the board.
        """
        return self.__width

    def get_height(self):
        """
        returns the height of the board.
        """
        return self.__height

    def get_coronas(self):
        """
        gets the list of corona locations.
        """
        return self.__coronas

    def set_first_mask(self, value):
        """
        sets the value of the first_mask field to the given value.
        """
        self.__first_mask = value

    def remove_mask_location(self, location):
        """
        removes a given location from the mask locations list.
        """
        self.__mask_locations.remove(location)
