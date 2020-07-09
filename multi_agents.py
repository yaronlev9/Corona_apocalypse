import math
import abc
import random
import game_state
from operator import itemgetter


class Agent(object):
    def __init__(self):
        super(Agent, self).__init__()

    @abc.abstractmethod
    def get_action(self, game_state):
        return

    def stop_running(self):
        pass


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
        return self.expectimax_helper(0, game_state, 0)[1]

    def expectimax_helper(self, current_depth, state, player):
        successors = []
        if current_depth == self.depth or state.get_done():
            return evaluation_function(state), game_state.Action.STOP
        if player == 0:
            legal_actions = state.get_legal_actions(0)
            for action in legal_actions:
                successors.append(
                    (state.generate_successor(0, action), action))
            lst = [(self.expectimax_helper(current_depth, successor[0], 1)[0],
                    successor[1]) for
                   successor in successors]
            lst = sorted(lst, key=itemgetter(0))
            return lst[0]
        else:
            legal_actions1 = state.get_legal_actions(1)
            for action1 in legal_actions1:
                temp_state = (state.generate_successor(1, action1), action1)
                legal_actions2 = temp_state[0].get_legal_actions(2)
                for action2 in legal_actions2:
                    temp_state2 = (temp_state[0].generate_successor(2, action2), action2)
                    legal_actions3 = temp_state2[0].get_legal_actions(3)
                    for action3 in legal_actions3:
                        successors.append((temp_state2[0].generate_successor(3, action3), action3))
            lst = [
                (self.expectimax_helper(current_depth + 1, successor[0], 0)[0],
                 successor[1]) for
                successor in successors]
            sum_of_sons = sum(child[0] for child in lst)
            avg = sum_of_sons / len(lst)
            return avg, game_state.Action.STOP


def evaluation_function(current_game_state):
    board = current_game_state.get_board()
    target = current_game_state.get_target()
    distance_from_target = pitagoras(target, current_game_state.get_location())
    distance_from_beginning = pitagoras(current_game_state.get_location(), (0, 15))
    distance_from_corona_1 = manhattan_distance(current_game_state.get_corona_1_location(),
                                                current_game_state.get_location())
    distance_from_corona_2 = manhattan_distance(current_game_state.get_corona_2_location(),
                                                current_game_state.get_location())
    distance_from_corona_3 = manhattan_distance(current_game_state.get_corona_3_location(),
                                                current_game_state.get_location())
    dist_from_mask_1 = 4
    dist_from_mask_2 = 4
    if len(current_game_state.get_mask_locations()) >= 1:
        dist_from_mask_1 = pitagoras(current_game_state.get_mask_locations()[0],
                                     current_game_state.get_location())
    if len(current_game_state.get_mask_locations()) >= 2:
        dist_from_mask_2 = pitagoras(current_game_state.get_mask_locations()[1],
                                     current_game_state.get_location())
    dist_from_closest_mask = min([dist_from_mask_1, dist_from_mask_2])
    # if current_game_state.get_mask_status():
    # if current_game_state.get_mask_status() and current_game_state.get_first_mask():
    #     current_game_state.set_first_mask(False)
    #     return -100000
    penalty = 1
    mask_reward = 1
    if not current_game_state.get_mask_status():
        if distance_from_corona_1 <= 2:
            penalty += 1.5
        elif distance_from_corona_1 <= 3:
            penalty += 1
        if distance_from_corona_2 <= 2:
            penalty += 1.5
        elif distance_from_corona_2 <= 3:
            penalty += 1
        if distance_from_corona_3 <= 2:
            penalty += 1.5
        elif distance_from_corona_3 <= 3:
            penalty += 1.5
    # if dist_from_closest_mask == 0:
    #     mask_reward /= 3
    # elif dist_from_closest_mask <= 2:
    #     mask_reward /= 2
    # elif dist_from_closest_mask == 3:
    #     mask_reward /= 1.25
    if distance_from_target == 0:
        return -1000000
    return (distance_from_target * 8 * penalty * mask_reward) + (distance_from_beginning * 1) + (
            2 * current_game_state.get_score())
    # return (dist_from_closest_mask * 11) + (distance_from_target * 5) - (distance_from_beginning * 5)


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

    def get_action(self, game_state):
        self.children = []
        self.num_simulations = 0
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
                for action1 in board_state.get_legal_actions(1):
                    state2 = board_state.generate_successor(1, action1)
                    for action2 in state2.get_legal_actions(2):
                        child = Node(board_state.generate_successor(2, action2), 0, cur_state)
                        leafs.append(child)
                        self.num_simulations += 1
                        result = self.run_simulation(child)
                        self.back_propagate(child, result)
                        if self.num_simulations == self.max_simulations:
                            return
            cur_state = random.choice(leafs)
            leafs.remove(cur_state)

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
            for i in range(500):
                board_state = board_state.generate_successor(0, random.choice(board_state.get_legal_actions(0)))
                board_state = board_state.generate_successor(1, random.choice(board_state.get_legal_actions(1)))
                board_state = board_state.generate_successor(2, random.choice(board_state.get_legal_actions(2)))
                if board_state.get_win():
                    return 0
                elif board_state.get_done():
                    return 1
            return 1
        elif state.player == 1:
            for i in range(500):
                board_state = board_state.generate_successor(1, random.choice(board_state.get_legal_actions(1)))
                board_state = board_state.generate_successor(2, random.choice(board_state.get_legal_actions(2)))
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
