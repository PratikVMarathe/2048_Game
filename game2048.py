import tkinter as tk
import random

# Initialize the game grid
def initialize_grid():
    grid = [[0] * 4 for _ in range(4)]
    add_new_tile(grid)
    add_new_tile(grid)
    return grid

# Add a new tile (2 or 4) to an empty spot in the grid
def add_new_tile(grid):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if grid[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        grid[i][j] = 2 if random.random() < 0.9 else 4

# Slide and merge logic for the rows
def slide_row_left(row):
    new_row = [num for num in row if num != 0]
    new_row += [0] * (4 - len(new_row))
    for i in range(3):
        if new_row[i] == new_row[i + 1] and new_row[i] != 0:
            new_row[i] *= 2
            new_row[i + 1] = 0
    new_row = [num for num in new_row if num != 0]
    new_row += [0] * (4 - len(new_row))
    return new_row

def move_left(grid):
    return [slide_row_left(row) for row in grid]

def move_right(grid):
    return [slide_row_left(row[::-1])[::-1] for row in grid]

def move_up(grid):
    transposed = list(zip(*grid))
    moved = move_left(transposed)
    return [list(row) for row in zip(*moved)]

def move_down(grid):
    transposed = list(zip(*grid))
    moved = move_right(transposed)
    return [list(row) for row in zip(*moved)]

# Check if the game is over
def is_game_over(grid):
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                return False
            if j < 3 and grid[i][j] == grid[i][j + 1]:
                return False
            if i < 3 and grid[i][j] == grid[i + 1][j]:
                return False
    return True

# GUI with tkinter
class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.grid = initialize_grid()

        # Create a 4x4 grid of labels
        self.tiles = [[None] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                tile = tk.Label(self.master, text="", width=4, height=2, font=("Helvetica", 24), bg="#cdc1b4", fg="#776e65")
                tile.grid(row=i, column=j, padx=5, pady=5)
                self.tiles[i][j] = tile

        self.update_grid_display()
        self.master.bind("<Key>", self.handle_keypress)

    def update_grid_display(self):
        for i in range(4):
            for j in range(4):
                value = self.grid[i][j]
                self.tiles[i][j].config(text=str(value) if value != 0 else "", bg=self.get_color(value))

    def get_color(self, value):
        colors = {
            0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
            256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e",
        }
        return colors.get(value, "#3c3a32")

    def handle_keypress(self, event):
        key = event.keysym
        if key == "Up":
            new_grid = move_up(self.grid)
        elif key == "Left":
            new_grid = move_left(self.grid)
        elif key == "Down":
            new_grid = move_down(self.grid)
        elif key == "Right":
            new_grid = move_right(self.grid)
        else:
            return

        if new_grid != self.grid:
            self.grid = new_grid
            add_new_tile(self.grid)
            self.update_grid_display()
            if is_game_over(self.grid):
                self.show_game_over()

    def show_game_over(self):
        game_over_label = tk.Label(self.master, text="Game Over!", font=("Helvetica", 36), bg="#bbada0", fg="#f9f6f2")
        game_over_label.grid(row=0, column=0, columnspan=4, rowspan=4)
        self.master.unbind("<Key>")

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
