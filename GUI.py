import tkinter as tk

SQUARE_SIZE = 37
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
        for row_index in range(initial_board.get_width()):
            self.canvas_list.append([])
            for col_index in range(initial_board.get_width()):
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
        counter = 1
        for corona in initial_board.get_coronas():
            name = "corona" + str(counter)
            self.make_label(name, corona, self.corona_img)
            counter += 1

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
        counter = 1
        for corona in state.get_coronas():
            name = "corona" + str(counter)
            self.change_pos(name, corona)
            counter += 1

    def destroy(self):
        self.root.destroy()