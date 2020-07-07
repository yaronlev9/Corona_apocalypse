import game_state
import multi_agents
import random


class Game(object):
    def __init__(self, agent, display):
        self.agent = agent
        self.display = display
        self._state = None
        self._should_quit = False

    def run(self, initial_state):
        self._should_quit = False
        self._state = initial_state
        # self.display.initialize(initial_state)
        return self._game_loop()

    def quit(self):
        self._should_quit = True

    def _game_loop(self):
        while not self._state.get_done() and not self._should_quit:
            # self.display.mainloop_iteration()
            action = self.agent.get_action(self._state)
            print(action)
            print(self._state)
            # action = random.choice(self._state.get_legal_actions(0))
            self._state.apply_action(action, 0)
            opponent_action1 = random.choice(self._state.get_legal_actions(1))
            self._state.apply_action(opponent_action1, 1)
            opponent_action2 = random.choice(self._state.get_legal_actions(2))
            self._state.apply_action(opponent_action2, 2)
            # self.display.update_state(self._state, action, opponent_action)
        print(self._state)
        print("winnnnnnn")
        return


ga = game_state.GameState()
agent = multi_agents.ExpectimaxAgent(3)
t = Game(agent, None)
t.run(ga)
