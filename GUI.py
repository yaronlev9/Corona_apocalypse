import tkinter as tk

SQUARE_SIZE = 37

WIDTH = 16
HEIGHT = 16
START_SCORE = 0
CITIZEN = '0'
CORONA_ILL_1 = '1'
CORONA_ILL_2 = '2'
CORONA_ILL_3 = '3'
WALL = '*'
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

    def create_board(self, initial_board):
        """
        creates a new board gui with a given initial board.
        """
        for row_index in range(WIDTH):
            self.canvas_list.append([])
            for col_index in range(HEIGHT):
                if initial_board.get_board()[row_index][col_index] == WALL:
                    self.canvas_list[row_index].append(
                        tk.Canvas(self.root, bg='gray30', width=SQUARE_SIZE, height=SQUARE_SIZE))
                else:
                    self.canvas_list[row_index].append(
                        tk.Canvas(self.root, bg='white', width=SQUARE_SIZE, height=SQUARE_SIZE))
                self.canvas_list[row_index][col_index].grid(row=row_index, column=col_index)
                if (row_index, col_index) == initial_board.get_target():
                    tk.Label(self.root, image=self.finish_img).grid(row=row_index, column=col_index)

    def make_label(self, row_index, col_index, image):
        label = tk.Label(self.root, image=image)
        label.grid(row=row_index, column=col_index)
        self.label_dict[(row_index, col_index)] = label

    def draw_state(self, state):
        """
        draws a given state on the gui board.
        """
        for row_index in range(len(state)):
            for col_index in range(len(state[row_index])):
                if (row_index, col_index) in self.label_dict:
                    self.label_dict[(row_index, col_index)].destroy()
                    self.label_dict.pop((row_index, col_index))
                if (15, 0) in self.label_dict:
                    tk.Label(self.root, image=self.finish_img).grid(row=15, column=0)
                    self.label_dict.pop((15, 0))
                if state[row_index][col_index] == CORONA_ILL_1 or state[row_index][col_index] == CORONA_ILL_2 or state[row_index][col_index] == CORONA_ILL_3:
                    self.make_label(row_index, col_index, self.corona_img)
                elif state[row_index][col_index] == CITIZEN:
                    self.make_label(row_index, col_index, self.player_img)
                elif state[row_index][col_index] == MASK:
                    self.make_label(row_index, col_index, self.mask_img)
