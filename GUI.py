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
        self.locations_dict = dict()
        self.masks_labels = dict()
        self.masks = initial_board.get_mask_locations().copy()
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
        for mask in self.masks:
            label = tk.Label(self.root, image=self.mask_img)
            label.grid(row=mask[0], column=mask[1])
            self.masks_labels[mask] = label
        self.make_players(initial_board)

    def make_players(self, initial_board):
        self.make_label("player", initial_board.get_location(), self.player_img)
        self.make_label("corona1", initial_board.get_corona_1_location(), self.corona_img)
        self.make_label("corona2", initial_board.get_corona_2_location(), self.corona_img)
        self.make_label("corona3", initial_board.get_corona_3_location(), self.corona_img)

    def make_label(self, string, location, image):
        label = tk.Label(self.root, image=image)
        label.grid(row=location[0], column=location[1])
        self.locations_dict[string] = label

    def change_pos(self, string, location):
        for mask in self.masks_labels.keys():
            if self.masks_labels[mask] != None and \
                    string == "player" and mask[0] == location[0] and mask[1] == location[1]:
                self.masks_labels[mask].destroy()
        self.locations_dict[string].grid(row=location[0], column=location[1])

    def draw_state(self, state):
        """
        draws a given state on the gui board.
        """
        self.change_pos("player", state.get_location())
        self.change_pos("corona1", state.get_corona_1_location())
        self.change_pos("corona2", state.get_corona_2_location())
        self.change_pos("corona3", state.get_corona_3_location())