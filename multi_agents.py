import game_state
from operator import itemgetter
from math import *


class ExpectimaxAgent:
    def __init__(self, depth):
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
            # print(lst)
            lst = sorted(lst, key=itemgetter(0))
            return lst[0]
        else:
            legal_actions1 = state.get_legal_actions(1)
            for action1 in legal_actions1:
                temp_state = (state.generate_successor(1, action1), action1)
                legal_actions2 = temp_state[0].get_legal_actions(2)
                for action2 in legal_actions2:
                    successors.append((temp_state[0].generate_successor(2, action2), action2))
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
    dist_from_mask_1 = pitagoras(current_game_state.get_mask_locations()[0],
                                          current_game_state.get_location())
    dist_from_mask_2 = pitagoras(current_game_state.get_mask_locations()[1],
                                          current_game_state.get_location())
    dist_from_closest_mask = min([dist_from_mask_1, dist_from_mask_2])
    if current_game_state.get_mask_status():
        return (distance_from_target * 8) + (distance_from_beginning * 1) + (2 *current_game_state.get_score())
    return (dist_from_closest_mask * 6) + (distance_from_target * 6)


def pitagoras(xy1, xy2):
    return sqrt((xy1[0] - xy2[0]) * (xy1[0] - xy2[0]) + (xy1[1] - xy2[1]) * (xy1[1] - xy2[1]))


def manhattan_distance(xy1, xy2):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

# ga = game_state.GameState()
# t = ExpectimaxAgent(1)
# print(t.get_action(ga))
