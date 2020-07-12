import game_state
import multi_agents
import random
import GUI

BOARD_16 =[
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
            ['*', '*', '*', '_', '*', '_', '*', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '*', '_', '_', '_', '*', '_', '*', '*', '*', '_', '_', '*'],
            ['_', '_', '_', '_', '*', '_', '_', '_', '*', '_', '_', '_', '*', '_', '_', '*'],
            ['_', '*', '_', '*', '*', '_', '*', '_', '*', '*', '*', '*', '*', '_', '*', '*'],
            ['_', '_', '_', '_', '_', '_', '*', '_', '_', '_', '_', '_', '_', '_', '*', '*']]

BOARD_12 = [
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['*', '_', '_', '_', '*', '*', '*', '*', '_', '_', '_', '_'],
            ['*', '*', '_', '_', '_', '_', '*', '*', '_', '*', '*', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '*', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '*', '*', '_'],
            ['_', '_', '_', '*', '*', '_', '*', '*', '_', '_', '_', '_'],
            ['*', '_', '*', '*', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['*', '_', '*', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['*', '_', '_', '_', '_', '_', '_', '_', '*', '*', '_', '_'],
            ['_', '_', '_', '_', '_', '*', '_', '*', '*', '_', '_', '*'],
            ['_', '*', '*', '_', '_', '*', '_', '*', '*', '_', '_', '*'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '*']]

BOARD_8 = [
            ['_', '_', '_', '*', '*', '_', '_', '_'],
            ['*', '_', '_', '_', '*', '*', '_', '_'],
            ['_', '_', '*', '_', '_', '_', '_', '_'],
            ['_', '_', '*', '_', '*', '*', '_', '_'],
            ['_', '_', '*', '_', '_', '*', '*', '*'],
            ['_', '*', '_', '_', '_', '*', '_', '*'],
            ['_', '*', '_', '_', '*', '_', '_', '*'],
            ['_', '_', '_', '_', '_', '_', '_', '_']]

BOARD_4 = [
            ['_', '_', '_', '_'],
            ['_', '*', '_', '_'],
            ['_', '_', '_', '_'],
            ['_', '_', '_', '_']]

# TARGET
# MASKS
# CORONAS
# WIDTH
# HEIGHT
# PLAYER
# TARGET
# BOARD

CORONA_4 = [(3,0), [(5, 4), (3,9)],[(0,0), (8,2)], 4, 4, (0,3), BOARD_4]
CORONA_8 = [(7,0), [(5, 4), (3,7)],[(0,0), (7,3)], 8, 8, (0,7), BOARD_8]
CORONA_12 = [(11,0), [(5, 4), (3,9)],[(0,0), (8,2), (5,10)], 12, 12, (0,11), BOARD_12]
CORONA_16 = [(15,0), [(5, 4), (3,9)],[(0,0), (8,2), (7,6)], 16, 16, (0,15), BOARD_16]

class Game(object):
    def __init__(self, agent, display):
        self.agent = agent
        self.display = display
        self._state = None
        self._should_quit = False

    def run(self, initial_state):
        self.display.root.update()
        self._should_quit = False
        self._state = initial_state
        return self._game_loop(initial_state)

    def quit(self):
        self._should_quit = True

    def _game_loop(self, initial_state):
        while not self._state.get_done() and not self._should_quit:
            action = self.agent.get_action(self._state)
            self._state.apply_action(action, 0)
            if self._state.get_win():
                break
            for corona in range(len(initial_state.get_coronas())):
                opponent_action = random.choice(self._state.get_legal_actions(corona + 1))
                self._state.apply_action(opponent_action, corona + 1)
            self.display.draw_state(self._state)
            self.display.root.update()
        if self._state.get_win():
            print("you won!!!")
        else:
            print("you lose :(")


if __name__ == '__main__':
    #ga = game_state.GameState(CORONA_4[0], CORONA_4[1], CORONA_4[2], CORONA_4[3], CORONA_4[4], CORONA_4[5], CORONA_4[6])
    #ga = game_state.GameState(CORONA_8[0], CORONA_8[1], CORONA_8[2], CORONA_8[3], CORONA_8[4], CORONA_8[5], CORONA_8[6])
    #ga = game_state.GameState(CORONA_12[0], CORONA_12[1], CORONA_12[2], CORONA_12[3], CORONA_12[4], CORONA_12[5], CORONA_12[6])
    ga = game_state.GameState(CORONA_16[0], CORONA_16[1], CORONA_16[2], CORONA_16[3], CORONA_16[4], CORONA_16[5], CORONA_16[6])
    #agent = multi_agents.MonteCarloTreeSearchAgent(150)
    agent = multi_agents.ExpectimaxAgent(2)
    t = Game(agent, GUI.Display(ga))
    t.run(ga)