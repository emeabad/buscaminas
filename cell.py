import random
from tkinter import *  # Button, Label, PhotoImage, TOP, font
from PIL import Image, ImageTk

import settings
import ctypes
import sys


class Cell:
    mines_discovered = 0
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y
        self.photo = ''
        # Append object
        Cell.all.append(self)

    def create_btn_object(self, location):
        self.photo = ImageTk.PhotoImage(Image.open('./assets/button.png'))
        btn = Button(
            location,
            width=23,
            height=23,
            image=self.photo
            # text=f'{self.x}, {self.y}'
        )
        btn.bind('<Button-1>', self.left_click_actions)  # left click
        btn.bind('<Button-3>', self.right_click_actions)  # Right click
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            text=f"LEFT:{Cell.cell_count}",
            font=("", 15)
        )
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        # print(event)
        if not self.is_opened:
            if self.is_mine:
                Cell.mines_discovered += 1
                self.show_mine()
            else:
                if self.surrounded_cells_mines_lenght == 0:
                    for cell_obj in self.surrounded_cells:
                        cell_obj.show_cell()
                self.show_cell()
                # if mines count is equal to the cells left count, player won
                if Cell.cell_count == settings.MINES_COUNT:
                    ctypes.windll.user32.MessageBoxW(0, 'Congratulations! You won the game', 'Game over', 0)

        # Cancel left and right click eentios if cell is already opened
        # self.cell_btn_object.unbind('<Button-1>')
        # self.cell_btn_object.unbind('<Button-3>')

    def get_cell_by_axys(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axys(self.x - 1, self.y - 1),
            self.get_cell_by_axys(self.x - 1, self.y),
            self.get_cell_by_axys(self.x - 1, self.y + 1),
            self.get_cell_by_axys(self.x, self.y - 1),
            self.get_cell_by_axys(self.x + 1, self.y - 1),
            self.get_cell_by_axys(self.x + 1, self.y),
            self.get_cell_by_axys(self.x + 1, self.y + 1),
            self.get_cell_by_axys(self.x, self.y + 1)
        ]
        cells = [cell for cell in cells if cell is not None]
        print(cells)
        return cells

    @property
    def surrounded_cells_mines_lenght(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1
        return counter

    def show_cell(self):
        if not self.is_opened:
            print('no estaba abierta')
            Cell.cell_count -= 1
            if self.surrounded_cells_mines_lenght == 0:
                self.photo = ImageTk.PhotoImage(Image.open('./assets/graybg.jpg'))
            else:
                self.photo = ImageTk.PhotoImage(Image.open(f"./assets/{self.surrounded_cells_mines_lenght}.png"))
            self.cell_btn_object.configure(
                # text=self.surrounded_cells_mines_lenght,
                # bg='gray',
                image=self.photo,
                width=23,
                height=23
            )
            # Replace the text of cell count label with the newer count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"LEFT: {Cell.cell_count}"
                )
            # If this was a mine candiadate, then for safety, we should
            # configure the background color to SystemButtonFace
            # self.cell_btn_object.configure(
                #bg='SystemButtonFace')
        self.is_opened = True

    def show_mine(self):
        self.is_opened = True
        self.photo = ImageTk.PhotoImage(Image.open(r"assets/mine.jpg"))
        self.cell_btn_object.configure(
            image=self.photo
        )
        ctypes.windll.user32.MessageBoxW(0, 'k-booom, You clicked on one mine', 'Game Over', 0)
        self.reset_game()

    def right_click_actions(self, event):
        if not self.is_opened:
            if not self.is_mine_candidate:
                self.photo = ImageTk.PhotoImage(Image.open(r"assets/candidate.png"))
                self.cell_btn_object.configure(
                    bg='orange',
                    image=self.photo
                )
                self.is_mine_candidate = True

            else:
                self.photo = ImageTk.PhotoImage(Image.open('./assets/graybg.gif'))
                self.cell_btn_object.configure(
                    # bg='SystemButtonFace',
                    image=self.photo
                )
                self.is_mine_candidate = False

    def reset_game(self):
        self.photo = ImageTk.PhotoImage(Image.open('./assets/button.png'))
        for cell in Cell.all:
            Cell.mines_discovered = 0
            cell.is_mine = False
            cell.is_opened = False
            cell.is_mine_candidate = False
            cell.cell_btn_object.configure(
                # bg='SystemButtonFace',
                image=self.photo,
                width=23,
                height=23
            )

        Cell.cell_count = settings.CELL_COUNT
        Cell.cell_count_label_object.configure(
            text=f"LEFT: {Cell.cell_count}"
        )
        self.randomize_mines()

    @staticmethod
    def randomize_mines():
        for cell in Cell.all:
            cell.is_mine = False

        picked_cells = random.sample(
            Cell.all,
            settings.MINES_COUNT
        )
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
