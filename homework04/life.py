import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = None,
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid: Grid = []
        for _ in range(self.rows):
            if randomize:
                row = [random.randint(0, 1) for _ in range(self.cols)]
            else:
                row = [0 for _ in range(self.cols)]
            grid.append(row)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        neighbours: Cells = []

        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                ny = row + dy
                nx = col + dx

                if 0 <= ny < self.rows and 0 <= nx < self.cols:
                    neighbours.append(self.curr_generation[ny][nx])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid: Grid = []
        for y in range(self.rows):
            new_row: Cells = []
            for x in range(self.cols):
                neighbours = self.get_neighbours((y, x))
                alive_neighbours = sum(neighbours)
                cell = self.curr_generation[y][x]

                if cell == 1:
                    if alive_neighbours in (2, 3):
                        new_row.append(1)
                    else:
                        new_row.append(0)
                else:
                    if alive_neighbours == 3:
                        new_row.append(1)
                    else:
                        new_row.append(0)
            new_grid.append(new_row)
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is None:
            return False
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid: Grid = []

        with filename.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                row: Cells = []
                for ch in line:
                    if ch in ("1", "*", "O"):
                        row.append(1)
                    else:
                        row.append(0)
                grid.append(row)
        rows = len(grid)
        cols = len(grid[0])

        life = GameOfLife(size=(rows, cols), randomize=False)
        life.curr_generation = grid
        life.prev_generation = [row[:] for row in grid]

        return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with filename.open("w", encoding="utf-8") as f:
            for row in self.curr_generation:
                line = "".join(str(cell) for cell in row)
                f.write(line + "\n")
