import tkinter as tk
from tkinter import messagebox, ttk
from typing import List

from maze import add_path_to_grid, bin_tree_maze, solve_maze


def draw_cell(x, y, color, size: int = 10):
    x *= size
    y *= size
    x1 = x + size
    y1 = y + size
    canvas.create_rectangle(x, y, x1, y1, fill=color)


def draw_maze(grid: List[List[str | int]], size: int = 10):
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == " ":
                color = "White"
            elif cell == "■":
                color = "black"
            elif cell == "X":
                color = "pink"
            draw_cell(y, x, color, size)


def show_solution():
    global GRID, N, M
    GRID = bin_tree_maze(N, M, random_exit=False)
    solved_grid, path = solve_maze(GRID)

    if path:
        maze_with_path = add_path_to_grid(GRID, path)
        draw_maze(maze_with_path, CELL_SIZE)
    else:
        messagebox.showerror("Ошибка", "Не удалось найти путь!")


if __name__ == "__main__":
    global GRID, CELL_SIZE, canvas
    N, M = 51, 77

    CELL_SIZE = 10
    GRID = bin_tree_maze(N, M, random_exit=False)

    window = tk.Tk()
    window.title("Maze")
    window.geometry("%dx%d" % (M * CELL_SIZE + 100, N * CELL_SIZE + 100))

    canvas = tk.Canvas(window, width=M * CELL_SIZE, height=N * CELL_SIZE)
    canvas.pack()

    draw_maze(GRID, CELL_SIZE)
    ttk.Button(window, text="Solve", command=show_solution).pack(pady=20)

    window.mainloop()
