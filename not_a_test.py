import game
import game_state
import time
import random
import multi_agents


def test_board(all_result, states, max_time):
    counter = 1
    for state in states:
        print("running state: ", counter)
        counter += 1
        result = []
        result_expectimax = []
        result_monte_carlo = []
        i = 0
        while i < 50:
            print(i)
            start = time.time()
            ga = game_state.GameState(state[0], state[1], state[2], state[3], state[4],
                                      state[5], state[6])
            agent = multi_agents.ExpectimaxAgent(2)
            t = game.Game(agent)
            res = t.run(ga, max_time)
            end = time.time()
            i += 1
            result_expectimax.append([res[0], end-start, res[1]])
        result.append(result_expectimax)
        i = 0
        while i < 50:
            print(i)
            start = time.time()
            ga = game_state.GameState(state[0], state[1], state[2], state[3], state[4],
                                      state[5], state[6])
            agent = multi_agents.MonteCarloTreeSearchAgent(150)
            t = game.Game(agent)
            res = t.run(ga, max_time)
            end = time.time()
            i += 1
            result_monte_carlo.append([res[0], end-start, res[1]])
        result.append(result_monte_carlo)
        all_result.append(result)

def run_all_test():
    # result_board_4 = []
    # corona_4_1 = [(3, 0), [(3, 3)], [(0, 0), (1, 2)], 4, 4, (0, 3), game.BOARD_4]
    # corona_4_2 = [(3, 0), [], [(1, 2)], 4, 4, (0, 3), game.BOARD_4]
    # states_4 = [corona_4_1, corona_4_2]
    # print("run test board 4")
    # test_board(result_board_4, states_4, None)
    # print("results test board 4:\n", result_board_4)
    # 1.5 minutes


    result_board_8 = []
    corona_8_1 = [(7, 0), [(5, 4)], [(3, 7), (7, 3)], 8, 8, (0, 7), game.BOARD_8]
    corona_8_2 = [(7, 0), [(0, 0)], [(4, 0), (7, 3)], 8, 8, (0, 7), game.BOARD_8]
    corona_8_3 = [(7, 0), [(7, 5)], [(1, 1), (7, 3)], 8, 8, (0, 7), game.BOARD_8]
    states_8 = [corona_8_1, corona_8_2, corona_8_3]
    print("run test board 8")
    test_board(result_board_8, states_8, 1)
    print("results test board 8:\n", result_board_8)

    # result_board_12 = []
    # corona_12_1 = [(11, 0), [(5, 4), (3, 9)], [(0, 0), (8, 2), (5, 10)], 12, 12, (0, 11), game.BOARD_12]
    # corona_12_2 = [(11, 0), [(5, 0), (11, 8)], [(3, 3), (8, 2), (2, 11)], 12, 12, (0, 11), game.BOARD_12]
    # corona_12_3 = [(11, 0), [(0, 0), (11, 8)], [(6, 6), (11, 2), (5, 10)], 12, 12, (0, 11), game.BOARD_12]
    # corona_12_4 = [(11, 0), [(3, 0), (10, 6)], [(11, 9), (8, 2), (6, 0)], 12, 12, (0, 11), game.BOARD_12]
    # states_12 = [corona_12_1, corona_12_2, corona_12_3, corona_12_4]
    # print("run test board 12")
    # test_board(result_board_12, states_12, 2)
    # print("results test board 12:\n", result_board_12)
    #
    # result_board_16 = []
    # corona_16_1 = [(15, 0), [(7, 15), (6, 0)], [(13, 13), (8, 2), (7, 7)], 16, 16, (0, 15), game.BOARD_16]
    # corona_16_2 = [(15, 0), [(2, 1), (10, 0)], [(7, 10), (13, 7), (0, 8)], 16, 16, (0, 15), game.BOARD_16]
    # corona_16_3 = [(15, 0), [(13, 11), (6, 4)], [(11, 10), (10, 2), (7, 7)], 16, 16, (0, 15), game.BOARD_16]
    # corona_16_4 = [(12, 0), [(7, 15), (14, 7)], [(0, 8), (5, 10), (12, 7)], 16, 16, (0, 15), game.BOARD_16]
    # corona_16_5 = [(15, 0), [(7, 9), (6, 0)], [(11, 2), (4, 3), (7, 7)], 16, 16, (0, 15), game.BOARD_16]
    # corona_16_6 = [(15, 0), [(9, 10), (0, 0)], [(3, 7), (9, 8), (13, 2)], 16, 16, (0, 15), game.BOARD_16]
    # states_16 = [corona_16_1, corona_16_2, corona_16_3, corona_16_4, corona_16_5, corona_16_6]
    # print("run test board 16")
    # test_board(result_board_16, states_16, 3)
    # print("results test board 16:\n", result_board_16)



if __name__ == '__main__':
    run_all_test()
