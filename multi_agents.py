from heapq import heappush, heappop
import math
import abc
import random
import game_state
from operator import itemgetter
import keyboard
from time import sleep


class Agent(object):
    """
    an abstract agent class.
    """
    def __init__(self):
        super(Agent, self).__init__()

    @abc.abstractmethod
    def get_action(self, game_state):
        """
        gets an action for a game state.
        """
        return

    def is_mask_state(self, state, masks_locations):
        """
        returns true iff the given state is a state where the player stands on a mask location.
        """
        return state.get_location() in masks_locations

    def is_goal_state(self, state):
        """
        returns true iff the state is a state where the player got to the target.
        """
        return state.get_target() == state.get_location()


class InteractiveAgent(Agent):
    """
    an agent for the game, that lets a player use the keyboard to play the game.
    """
    def __init__(self):
        super().__init__()

    def get_action(self, state):
        """
        gets a possible action for a given game state.
        """
        sleep(0.2)
        while True:
            if keyboard.is_pressed('s'):
                return game_state.Action.DOWN
            if keyboard.is_pressed('w'):
                return game_state.Action.UP
            if keyboard.is_pressed('d'):
                return game_state.Action.RIGHT
            if keyboard.is_pressed('a'):
                return game_state.Action.LEFT


class ExpectimaxAgent(Agent):
    """
    an agent that implements the Expectimax algorithm in order to solve the board.
    """
    def __init__(self, depth):
        super().__init__()
        self.depth = depth

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        if game_state.get_mask_status():
            if game_state.get_location() in game_state.get_mask_locations():
                game_state.remove_mask_location(game_state.get_location())
                game_state.set_first_mask(False)
        return self.expectimax(0, game_state, 0)[1]

    def expectimax(self, current_depth, state, player):
        """
        the expectimax algorithm implementation.
        """
        successors = []
        if current_depth == self.depth or state.get_done():
            return self.evaluation_function(state), game_state.Action.STOP
        if player == 0:
            legal_actions = state.get_legal_actions(0)
            for action in legal_actions:
                successors.append(
                    (state.generate_successor(0, action), action))
            lst = [(self.expectimax(current_depth, successor[0], 1)[0],
                    successor[1]) for
                   successor in successors]
            lst = sorted(lst, key=itemgetter(0))
            highest_evaluation_list = []
            for pair in lst:
                if pair[0] == lst[0][0]:
                    highest_evaluation_list += [pair]
                else:
                    break
            return random.choice(highest_evaluation_list)
        else:
            successors += self.expectimax_helper((state, game_state.Action.STOP), len(state.get_coronas()), [])
            lst = [
                (self.expectimax(current_depth + 1, successor[0], 0)[0],
                 successor[1]) for
                successor in successors]
            sum_of_sons = sum(child[0] for child in lst)
            avg = sum_of_sons / len(lst)
            return avg, game_state.Action.STOP

    def expectimax_helper(self, state, coronas, lst):
        """
        a helper for expectimax, that implements a recursive part of the algorithm.
        """
        if coronas == 0:
            return
        for action in state[0].get_legal_actions(coronas):
            temp_state = (state[0].generate_successor(coronas, action), action)
            self.expectimax_helper(temp_state, coronas - 1, lst)
            if coronas == 1:
                lst.append(temp_state)
        if len(state[0].get_coronas()) == coronas:
            return lst

    def evaluation_function(self, current_game_state):
        """"
        evaluates the credibility of a given state for expectimax algorithm.
        """
        board = current_game_state.get_board()
        target = current_game_state.get_target()
        distance_from_target = pitagoras(target, current_game_state.get_location())
        dist_from_mask_1 = 4
        dist_from_mask_2 = 4
        closest_mask_location = None
        if len(current_game_state.get_mask_locations()) >= 1:
            dist_from_mask_1 = manhattan_distance(current_game_state.get_mask_locations()[0],
                                                  current_game_state.get_location())
            closest_mask_location = current_game_state.get_mask_locations()[0]
        if len(current_game_state.get_mask_locations()) >= 2:
            dist_from_mask_2 = manhattan_distance(current_game_state.get_mask_locations()[1],
                                                  current_game_state.get_location())
            if dist_from_mask_1 > dist_from_mask_2:
                closest_mask_location = current_game_state.get_mask_locations()[1]
        corona_penalty = get_corona_penalty(current_game_state, board)
        mask_reward = get_mask_reward(dist_from_mask_1, dist_from_mask_2, current_game_state, closest_mask_location)
        penalize_mask = random.choice([0, 1, 2])
        walls_penalty = penalty(current_game_state.get_target(), current_game_state.get_location(), board,
                                current_game_state.get_width() - 1) if penalize_mask else 1
        return distance_from_target * corona_penalty * mask_reward + walls_penalty


def get_walls_penalty(target, location, board, addition, size):
    """
    a heuristic function used by the evaluation function, that penalizes a state credibility if there is
    a wall between the player and the target.
    """
    penalty = 1
    if location[0] < size and target[0] > location[0] and board[location[0] + 1][location[1]] == '*':
        penalty += addition
    if location[1] > 0 and target[1] < location[1] and board[location[0]][location[1] - 1] == '*':
        penalty += addition
    return penalty


def penalty(target, location, board, size):
    """
     a heuristic function used by the evaluation function, that penalizes a state credibility if there is
    a wall between the player and the target.
    """
    penalty = get_walls_penalty(target, location, board, 2, size)
    if location[0] < size and board[location[0] + 1][location[1]] != '*':
        penalty += get_walls_penalty(target, (location[0] + 1, location[1]), board, 0.25, size)
    if location[1] > 0 and board[location[0]][location[1] - 1] != '*':
        penalty += get_walls_penalty(target, (location[0], location[1] - 1), board, 0.25, size)
    if location[0] > 0 and board[location[0] - 1][location[1]] != '*':
        penalty += get_walls_penalty(target, (location[0] - 1, location[1]), board, 0.25, size)
    if location[1] < size and board[location[0]][location[1] + 1] != '*':
        penalty += get_walls_penalty(target, (location[0], location[1] + 1), board, 0.25, size)
    return penalty


def wall_between_points(first_point, second_point, board):
    """
    checks if there are walls between two points on the board.
    """
    horizontal_dist = abs(first_point[1] - second_point[1])
    vertical_dist = abs(first_point[0] - second_point[0])
    min_horizontal = min(first_point[1], second_point[1])
    min_vertical = min(first_point[0], second_point[0])
    for j in range(vertical_dist + 1):
        for i in range(horizontal_dist - 1):
            if board[min_vertical + j][min_horizontal + i + 1] == '*':
                return True
    for i in range(horizontal_dist + 1):
        for j in range(vertical_dist - 1):
            if board[min_vertical + j + 1][min_horizontal + i] == '*':
                return True
    return False


def get_mask_reward(dist_from_mask_1, dist_from_mask_2, state, closest_mask_location):
    """
    a heuristic function, used by the evaluation function to get a reward for states with a mask close to them.
    """
    mask_reward = 1
    dist_from_closest_mask = min([dist_from_mask_1, dist_from_mask_2])
    if closest_mask_location is not None and not wall_between_points(state.get_location(), closest_mask_location,
                                                                     state.get_board()) and state.get_first_mask():
        if dist_from_closest_mask < 2:
            mask_reward /= 1.5
        elif dist_from_closest_mask <= 2:
            mask_reward /= 1.3
        elif dist_from_closest_mask == 3:
            mask_reward /= 1.1
    return mask_reward


def get_corona_penalty(current_game_state, board):
    """
     a heuristic function, used by the evaluation function to get a penalty for states that a corona virus is
     close to the player.
    """
    penalty = 1
    coronas = current_game_state.get_coronas()
    distance_lst = [manhattan_distance(corona, current_game_state.get_location())
                    for corona in coronas]
    if not current_game_state.get_mask_status():
        for index in range(len(distance_lst)):
            if distance_lst[index] <= 3 and not wall_between_points(current_game_state.get_location(),
                                                                    current_game_state.get_coronas()[index], board):
                if distance_lst[index] <= 2:
                    penalty += 1.5
                elif distance_lst[index] <= 3:
                    penalty += 1
    return penalty


def pitagoras(xy1, xy2):
    """
    calculates the pitagorean distance between two points on the board.
    """
    return math.sqrt((xy1[0] - xy2[0]) * (xy1[0] - xy2[0]) + (xy1[1] - xy2[1]) * (xy1[1] - xy2[1]))


def manhattan_distance(xy1, xy2):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


class Node():
    """
    a class that represents a node in the game tree.
    """
    def __init__(self, state, player, parent):
        self.counter = 0
        self.wins = 0
        self.state = state
        self.player = player
        self.parent = parent
        self.simulations_counter = 0
        self.total_simulations = 0

    def __lt__(self, other):
        return calculate_score(self) < calculate_score(other)

    def set_simulations(self, num):
        self.total_simulations = num


class MonteCarloTreeSearchAgent(Agent):
    """
    an MCST agent to solve the game.
    """

    def __init__(self, max_simulations):
        super().__init__()
        self.max_simulations = max_simulations
        self.root = None
        self.num_of_nodes = 5
        self.num_coronas = 0

    def get_action(self, game_state):
        """
        gets an action for a given state.
        """
        self.children = []
        self.children_to_explore = []
        self.num_simulations = 0
        self.num_coronas = len(game_state.get_coronas())
        self.root = Node(game_state, 0, None)
        if not game_state.get_mask_status():
            self.closest_target = closest_target(find_masks(game_state.get_board(), game_state.get_mask_locations()) +
                                                 [game_state.get_target()], game_state.get_location(),
                                                 game_state.get_board())[0]
        else:
            self.closest_target = closest_target([game_state.get_target()], game_state.get_location(),
                                                 game_state.get_board())[0]
        self.monte_carlo_tree_search(self.root)
        best = self.best_child()
        return best[1]

    def monte_carlo_tree_search(self, state):
        """
        the implementation of MCST algorithm.
        """
        leafs = []
        cur_state = state
        board_state = cur_state.state
        while self.num_simulations < self.max_simulations:
            player = cur_state.player
            if player == 0:
                lst = board_state.get_legal_actions(0)
                random.shuffle(lst)
                for action in board_state.get_legal_actions(0):
                    child = Node(board_state.generate_successor(0, action), 1, cur_state)
                    self.num_simulations += 1
                    child.set_simulations(self.num_simulations)
                    if cur_state is self.root:
                        self.children.append((child, action))
                        self.children_to_explore.append(child)
                    num_moves = int(manhattan_distance(child.state.get_location(), self.closest_target) * 1.5)
                    result, cause = self.run_simulation(child, num_moves)
                    self.back_propagate(child, result, cause)
                    heappush(leafs, child)
                    if self.num_simulations == self.max_simulations:
                        return
            else:
                successors = self.monte_carlo_helper(board_state, self.num_coronas, [], cur_state)
                size = self.num_of_nodes
                if len(successors) < self.num_of_nodes:
                    size = len(successors)
                for i in range(size):
                    child = random.choice(successors)
                    successors.remove(child)
                    self.num_simulations += 1
                    child.set_simulations(self.num_simulations)
                    num_moves = int(manhattan_distance(child.state.get_location(), self.closest_target) * 1.5)
                    res, cause = self.run_simulation(child, num_moves)
                    self.back_propagate(child, res, cause)
                    heappush(leafs, child)
                    if self.num_simulations == self.max_simulations:
                        return
            if len(self.children_to_explore) == 0:
                cur_state = heappop(leafs)
            else:
                cur_state = self.children_to_explore.pop()
            board_state = cur_state.state

    def monte_carlo_helper(self, state, coronas, lst, parent):
        if coronas == 0:
            return
        for action in state.get_legal_actions(coronas):
            temp_state = state.generate_successor(coronas, action)
            self.monte_carlo_helper(temp_state, coronas - 1, lst, parent)
            if coronas == 1:
                lst.append(Node(temp_state, 0, parent))
        if self.num_coronas == coronas:
            return lst

    def back_propagate(self, node, result, cause=None):
        """
        the back propagation part of the algorithm, that updates the game tree upwards.
        """
        while node != None:
            if result == 1 and node.player == 0:
                node.wins += 50
            elif result == 0 and node.player == 1:
                if cause == "mask" or cause is None:
                    node.wins += 10
                else:
                    node.wins += 50
            node.simulations_counter += 1
            node = node.parent

    def run_simulation(self, state, num_of_moves):
        """
        runs a simulation for MCST state.
        """
        board_state = state.state
        if state.player == 0:
            for i in range(num_of_moves):
                board_state = board_state.generate_successor(0, random.choice(board_state.get_legal_actions(0)))
                for j in range(self.num_coronas):
                    board_state = board_state.generate_successor(j + 1,
                                                                 random.choice(board_state.get_legal_actions(j + 1)))
                if self.is_goal_state(board_state):
                    return (0, "syringe")
                if self.is_mask_state(board_state, [self.closest_target]):
                    return (0, "mask")
                elif board_state.get_done():
                    return (1, None)
            return (1, None)
        elif state.player == 1:
            for i in range(num_of_moves):
                for j in range(self.num_coronas):
                    board_state = board_state.generate_successor(j + 1,
                                                                 random.choice(board_state.get_legal_actions(j + 1)))
                board_state = board_state.generate_successor(0, random.choice(board_state.get_legal_actions(0)))
                if self.is_goal_state(board_state):
                    return (0, "syringe")
                if self.is_mask_state(board_state, [self.closest_target]):
                    return (0, "mask")
                elif board_state.get_done():
                    return (1, None)
            return (1, None)

    def best_child(self):
        """
        gets the best child state of the current state in the game.
        """
        flag = True
        for child in range(len(self.children) - 1):
            if calculate_score(self.children[child][0]) != calculate_score(self.children[child + 1][0]):
                flag = False
                break
        if flag:
            return random.choice(self.children)
        min = math.inf
        best_state = None
        for state in self.children:
            score = calculate_score(state[0])
            if score < min or best_state is None:
                min = score
                best_state = state
        return best_state


def closest_target(targets, location, board):
    """
    finds the closest semi target to the player on the board.
    """
    min = None
    closest_target = None
    for target in targets:
        distance = manhattan_distance(location, target)
        if min is None or distance < min:
            min = distance
            closest_target = target
    if min > 5:
        lst, closer_cells = find_empty_cells(board, location)
        random.shuffle(lst)
        flag = False
        for item in lst:
            if (closest_target[0] >= item[0] >= location[0] and closest_target[1] >= item[1] >= location[1]):
                cur_min = pitagoras(location, item)
                if cur_min <= 5:
                    min = cur_min
                    closest_target = item
                    flag = True
                    break
            elif (closest_target[0] >= item[0] >= location[0] and location[1] >= item[1] >= closest_target[1]):
                cur_min = manhattan_distance(location, item)
                if cur_min <= 5:
                    min = cur_min
                    closest_target = item
                    flag = True
                    break
            elif (location[0] >= item[0] >= closest_target[0] and closest_target[1] >= item[1] >= location[1]):
                cur_min = manhattan_distance(location, item)
                if cur_min <= 5:
                    min = cur_min
                    closest_target = item
                    flag = True
                    break
            elif (location[0] >= item[0] >= closest_target[0] and location[1] >= item[1] >= closest_target[1]):
                cur_min = manhattan_distance(location, item)
                if cur_min <= 5:
                    min = cur_min
                    closest_target = item
                    flag = True
                    break
        if not flag:
            cell = random.choice(closer_cells)
            min = pitagoras(location, cell)
            closest_target = cell
            # break
    return closest_target, min


def calculate_score(state):
    """
    calculates the current score of the player.
    """
    if state.simulations_counter == 0:
        return math.inf
    score = -(state.wins / state.simulations_counter) + \
            math.sqrt(2) * (math.log(state.total_simulations) / state.simulations_counter)
    return score


def find_masks(board, masks):
    """
    finds the mask locations on the board.
    """
    lst = []
    for mask in masks:
        if board[mask[0]][mask[1]] == 'm':
            lst.append(mask)
    return lst


def find_empty_cells(board, location):
    lst1 = []
    lst2 = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == "_" and 1 <= manhattan_distance(location, (row, col)) <= 5:
                lst1.append((row, col))
            if board[row][col] == "_" and 1 <= pitagoras(location, (row, col)) <= 2:
                lst2.append((row, col))
    return lst1, lst2
