import tkinter as tk

SQUARE_SIZE = 37

WIDTH = 16
HEIGHT = 16
START_SCORE = 0
CITIZEN = '0'
CORONA_ILL_1 = '1'
CORONA_ILL_2 = '2'
WALL = '-'
EMPTY_LOCATION = '_'
TARGET = 'W'
MASK = 'm'


class Display:

    def __init__(self, initial_board):
        self.root = tk.Tk()
        self.root.resizable(True, True)
        self.canvas_list = []
        self.finish_img = tk.PhotoImage(file="images//syringe.png")
        self.player_img = tk.PhotoImage(file="images//doctor.png")
        self.corona_img = tk.PhotoImage(file="images//corona.png")
        self.mask_img = tk.PhotoImage(file="images//mask.png")
        self.label_dict = dict()
        self.create_board(initial_board)

    def draw_rectangle(self, row_index, col_index, color):
        self.canvas_list[row_index][col_index].create_rectangle((SQUARE_SIZE * row_index, SQUARE_SIZE * col_index),
                                                                (SQUARE_SIZE * (row_index + 1),
                                                                 SQUARE_SIZE * (col_index + 1)),
                                                                fill=color)

    def create_board(self, initial_board):
        for row_index in range(WIDTH):
            self.canvas_list.append([])
            for col_index in range(HEIGHT):
                if initial_board[row_index][col_index] == WALL:
                    self.canvas_list[row_index].append(
                        tk.Canvas(self.root, bg='gray30', width=SQUARE_SIZE, height=SQUARE_SIZE))
                else:
                    self.canvas_list[row_index].append(
                        tk.Canvas(self.root, bg='white', width=SQUARE_SIZE, height=SQUARE_SIZE))
                self.canvas_list[row_index][col_index].grid(row=row_index, column=col_index)
                if initial_board[row_index][col_index] == TARGET:
                    tk.Label(self.root, image=self.finish_img).grid(row=row_index, column=col_index)

    def draw_state(self, state):
        for row_index in range(len(state)):
            for col_index in range(len(state[row_index])):
                if state[row_index][col_index] == CORONA_ILL_1 or state[row_index][col_index] == CORONA_ILL_2:
                    label = tk.Label(self.root, image=self.corona_img)
                    label.grid(row=row_index, column=col_index)
                    self.label_dict[(row_index, col_index)] = label
                elif state[row_index][col_index] == CITIZEN:
                    label = tk.Label(self.root, image=self.player_img)
                    label.grid(row=row_index, column=col_index)
                    self.label_dict[(row_index, col_index)] = label
                elif state[row_index][col_index] == MASK:
                    label = tk.Label(self.root, image=self.mask_img)
                    label.grid(row=row_index, column=col_index)
                    self.label_dict[(row_index, col_index)] = label
                elif state[row_index][col_index] != WALL and state[row_index][col_index] != TARGET \
                        and (row_index, col_index) in self.label_dict:
                    self.label_dict[(row_index, col_index)].destroy()
                    self.label_dict.pop((row_index, col_index), None)

# simple test to check the code
if __name__ == '__main__':
    board = [
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '0'],
        ['-', '-', '-', '_', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '_', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '_', '-', '-', '-', 'm', '_', '_', '_', '_', '-', '-', '-', '-'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '-', '-', '-', '_', '-', '-', '-', '-'],
        ['_', '-', '-', '_', '-', '-', '-', '-', '-', '_', '-', '_', '-', '-', '-', '-'],
        ['_', '-', '_', '_', '-', '1', '_', '_', '_', '_', '-', '_', '-', '-', '-', '-'],
        ['-', '-', '_', '-', '-', '_', '_', '_', '_', '_', '-', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '-', '_', '_', '-', '-', '-', '-', '-', '-', '-', '_', '-', '-'],
        ['_', '-', '-', '-', '-', '_', '_', '_', '_', '_', '_', '_', '-', '_', '-', '-'],
        ['_', '_', '_', '_', '_', '_', '-', '_', '-', '_', '-', '-', '-', '_', '-', '-'],
        ['-', '-', '-', '_', '-', '_', '-', '_', '-', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', 'm', '-', '_', '-', '_', '-', '_', '-', '-', '-', '_', '-', '-'],
        ['2', '_', '_', '_', '-', '_', '-', '_', '-', '_', '_', '_', '-', '_', '-', '-'],
        ['_', '-', '-', '-', '-', '_', '-', '_', '-', '-', '-', '-', '-', '_', '-', '-'],
        ['W', '_', '_', '_', '_', '_', '-', '_', '_', '_', 'm', '_', '_', '_', '-', '-']]
    # new_board = [
    #     ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '0', '_'],
    #     ['-', '-', '-', '_', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    #     ['-', '-', '-', '_', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    #     ['-', '-', '-', '_', '-', '-', '-', '_', '_', '_', '_', '_', '-', '-', '-', '-'],
    #     ['_', '_', '_', '_', '_', '_', '_', '_', '-', '-', '-', '_', '-', '-', '-', '-'],
    #     ['_', '-', '-', '_', '-', '-', '-', '-', '-', '_', '-', '_', '-', '-', '-', '-'],
    #     ['_', '-', '_', '_', '-', '_', '1', '_', '_', '_', '-', '_', '-', '-', '-', '-'],
    #     ['-', '-', '_', '-', '-', '_', '_', '_', '_', '_', '-', '_', '_', '_', '_', '_'],
    #     ['_', '_', '_', '-', '_', '_', '-', '-', '-', '-', '-', '-', '-', '_', '-', '-'],
    #     ['_', '-', '-', '-', '-', '_', '_', '_', '_', '_', '_', '_', '-', '_', '-', '-'],
    #     ['_', '_', '_', '_', '_', '_', '-', '_', '-', '_', '-', '-', '-', '_', '-', '-'],
    #     ['-', '-', '-', '_', '-', '_', '-', '_', '-', '_', '_', '_', '_', '_', '_', '_'],
    #     ['_', '_', '_', '_', '-', '_', '-', '_', '-', '_', '-', '-', '-', '_', '-', '-'],
    #     ['2', '_', '_', '_', '-', '_', '-', '_', '-', '_', '_', '_', '-', '_', '-', '-'],
    #     ['_', '-', '-', '-', '-', '_', '-', '_', '-', '-', '-', '-', '-', '_', '-', '-'],
    #     ['W', '_', '_', '_', '_', '_', '-', '_', '_', '_', '_', '_', '_', '_', '-', '-']]
    display = Display(board)
    display.draw_state(board)
    # display.draw_state(new_board)
    display.root.mainloop()
