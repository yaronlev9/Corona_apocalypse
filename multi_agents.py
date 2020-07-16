import math
import abc
import random
import game_state
from operator import itemgetter
import keyboard
from time import sleep


class Agent(object):
    def __init__(self):
        super(Agent, self).__init__()

    @abc.abstractmethod
    def get_action(self, game_state):
        return

    def stop_running(self):
        pass

    def is_mask_state(self, state):
        return state.get_location() in state.get_mask_locations()

    def is_goal_state(self, state):
        return state.get_target() == state.get_location()


class InteractiveAgent(Agent):
    def __init__(self):
        super().__init__()

    def get_action(self, state):
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
    def __init__(self, depth):
        super().__init__()
        self.depth = depth

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        """*** YOUR CODE HERE ***"""
        if game_state.get_mask_status():
            if game_state.get_location() in game_state.get_mask_locations():
                game_state.remove_mask_location(game_state.get_location())
                game_state.set_first_mask(False)
        return self.expectimax(0, game_state, 0)[1]

    def expectimax(self, current_depth, state, player):
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
        board = current_game_state.get_board()
        target = current_game_state.get_target()
        distance_from_target = pitagoras(target, current_game_state.get_location())
        if self.is_goal_state(current_game_state):
            return -1000000
        # if self.is_mask_state(current_game_state):
        #     return -1000000
        distance_from_beginning = pitagoras(current_game_state.get_location(), (0, 15))
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

        # if current_game_state.get_mask_status():
        # if current_game_state.get_mask_status() and current_game_state.get_first_mask():
        #     current_game_state.set_first_mask(False)
        #     return -1000000
        corona_penalty = get_corona_penalty(current_game_state, board)
        mask_reward = get_mask_reward(dist_from_mask_1, dist_from_mask_2, current_game_state, closest_mask_location)
        walls_penalty = penalty(current_game_state.get_target(), current_game_state.get_location(), board,
                                current_game_state.get_width() - 1)
        # if current_game_state.get_location() == (9, 8):
        #     print("right = ", res)
        # elif current_game_state.get_location() == (9, 6):
        #     print("left = ", res)
        # elif current_game_state.get_location() == (10, 7):
        #     print("down = ", res)
        return distance_from_target * corona_penalty * mask_reward + walls_penalty
        # return (dist_from_closest_mask * 11) + (distance_from_target * 5) - (distance_from_beginning * 5)


def get_walls_penalty(target, location, board, addition, size):
    penalty = 1
    if location[0] < size and target[0] > location[0] and board[location[0] + 1][location[1]] == '*':
        penalty += addition
    if location[1] > 0 and target[1] < location[1] and board[location[0]][location[1] - 1] == '*':
        penalty += addition
    return penalty


def penalty(target, location, board, size):
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
    return math.sqrt((xy1[0] - xy2[0]) * (xy1[0] - xy2[0]) + (xy1[1] - xy2[1]) * (xy1[1] - xy2[1]))


def manhattan_distance(xy1, xy2):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


class Node:
    def __init__(self, state, player, parent):
        self.counter = 0
        self.wins = 0
        self.state = state
        self.player = player
        self.parent = parent
        self.simulations_counter = 0


class MonteCarloTreeSearchAgent(Agent):

    def __init__(self, max_simulations):
        super().__init__()
        self.max_simulations = max_simulations
        self.exploration_param = math.sqrt(2)
        self.root = None
        self.num_of_nodes = 3
        self.num_coronas = 0

    def get_action(self, game_state):
        self.children = []
        self.num_simulations = 0
        self.num_coronas = len(game_state.get_coronas())
        self.root = Node(game_state, 0, None)
        self.monte_carlo_tree_search(self.root, 0)
        return self.best_child()[1]

    def monte_carlo_tree_search(self, state, player):
        leafs = []
        cur_state = state
        board_state = state.state
        while self.num_simulations < self.max_simulations:
            player = cur_state.player
            if player == 0:
                for action in board_state.get_legal_actions(0):
                    child = Node(board_state.generate_successor(0, action), 1, cur_state)
                    leafs.append(child)
                    if cur_state is self.root:
                        self.children.append((child, action))
                    self.num_simulations += 1
                    result = self.run_simulation(child)
                    self.back_propagate(child, result)
                    if self.num_simulations == self.max_simulations:
                        return
            else:
                successors = self.monte_carlo_helper(board_state, self.num_coronas, [], cur_state)
                for child in successors:
                    leafs.append(child)
                    self.num_simulations += 1
                    result = self.run_simulation(child)
                    self.back_propagate(child, result)
                    if self.num_simulations == self.max_simulations:
                        return
            cur_state = random.choice(leafs)
            leafs.remove(cur_state)

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

    def back_propagate(self, node, result):
        while node.parent != None:
            if result == 0 and node.player == 0:
                node.wins += 1
            elif result == 1 and node.player == 1:
                node.wins += 1
            node.simulations_counter += 1
            node = node.parent

    def run_simulation(self, state):
        board_state = state.state
        if state.player == 0:
            for i in range(50):
                board_state = board_state.generate_successor(0, random.choice(board_state.get_legal_actions(0)))
                for j in range(self.num_coronas):
                    board_state = board_state.generate_successor(j + 1,
                                                                 random.choice(board_state.get_legal_actions(j + 1)))
                if board_state.get_win():
                    return 0
                elif board_state.get_done():
                    return 1
            return 1
        elif state.player == 1:
            for i in range(50):
                for j in range(self.num_coronas):
                    board_state = board_state.generate_successor(j + 1,
                                                                 random.choice(board_state.get_legal_actions(j + 1)))
                board_state = board_state.generate_successor(0, random.choice(board_state.get_legal_actions(0)))
                if board_state.get_win():
                    return 0
                elif board_state.get_done():
                    return 1
            return 1

    def best_child(self):
        max = 0
        best_state = None
        for state in self.children:
            score = self.calculate_score(state[0])
            if score > max:
                max = score
                best_state = state
        return best_state

    def calculate_score(self, state):
        score = (state.wins / state.simulations_counter) + \
                self.exploration_param * math.sqrt(math.log((self.num_simulations), math.e) / state.simulations_counter)
        return score
