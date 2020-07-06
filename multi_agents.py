import game_state


def evaluation_function(current_game_state):
    board = current_game_state.get_board()
    target = current_game_state.get_target()