from tkinter import *
from cell import Cell
import settings
import utils

# root is the convention for principal window
root = Tk()

# Override window config
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
root.title(settings.TITLE_WINDOW)
# root.configure(bg="black")
root.resizable(False, False)

# TOP FRAME
top_frame = Frame(
    root,
    width=settings.WIDTH,
    height=utils.height_prct(25)
)
top_frame.place(x=0, y=0)



# PRINCIPAL FRAME
center_frame = Frame(
    root,
    width=settings.WIDTH,
    height=utils.height_prct(75)
)
center_frame.place(
    x=utils.width_prct(5),
    y=utils.height_prct(25)
)

# Create cells
for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Cell(x, y)
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(
            column=y,
            row=x
        )

# Call the label
Cell.create_cell_count_label(top_frame)
Cell.cell_count_label_object.place(
    x=utils.width_prct(25)
)

# Random mines in the game
Cell.randomize_mines()

# print(Cell.all)
# Run the window
root.mainloop()
