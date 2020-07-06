import tkinter as tk

WIDTH = 16
HEIGHT = 16
START_SCORE = 0
CITIZEN = 1
CORONA_ILL = 2
WALL = '-'
EMPTY_LOCATION = '_'
TARGET = 'W'


class Display:

    def __init__(self, initial_board):
        self.root = tk.Tk()
        self.finish_img = tk.PhotoImage(file='finish.png')
        self.canvas_list = []
        self.create_board(initial_board)

    def draw_rectangle(self, row_index, col_index, color):
        self.canvas_list[row_index][col_index].create_rectangle((50 * row_index, 50 * col_index),
                                                                (50 * (row_index + 1), 50 * (col_index + 1)),
                                                                fill=color)

    def create_board(self, initial_board):
        for row_index in range(16):
            self.canvas_list.append([])
            for col_index in range(16):
                self.canvas_list.append(tk.Canvas(self.root, bg='white', width=50, height=50))
                self.canvas_list[row_index][col_index].grid(row=row_index, column=col_index)
                if initial_board[row_index][col_index] == WALL:
                    self.draw_rectangle(row_index, col_index, 'gray30')
                elif initial_board[row_index][col_index] == TARGET:
                    self.canvas_list[row_index][col_index].create_image(
                        50, 50, image=tk.PhotoImage(file='Corona_apocalypse/finish.png'))

    def draw_state(self, state):
        for row_index in range(len(state)):
            for col_index in range(len(state[row_index])):
                if state[row_index][col_index] == CORONA_ILL:
                    # insert corona image
                    pass
                elif state[row_index][col_index] == CITIZEN:
                    # insert citizen image
                    pass
