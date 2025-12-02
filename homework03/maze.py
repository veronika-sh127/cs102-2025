from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """

    x, y = coord
    rows, cols = len(grid), len(grid[0])
    available_directions = []

    if x > 1:
        available_directions.append("up")
    if y < cols - 2:
        available_directions.append("right")
    if not available_directions:
        return grid

    direction = choice(available_directions)
    if direction == "up":
        grid[x - 1][y] = " "
    else:
        grid[x][y + 1] = " "

    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for coord in empty_cells:
        remove_wall(grid, coord)

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = (
            randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
        )
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """

    exits = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if grid[x][y] == "X":
                exits.append((x, y))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> bool:
    """

    :param grid:
    :param k:
    :return:
    """

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == k:
                neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                for nx, ny in neighbors:
                    if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                        if grid[nx][ny] == 0:
                            grid[nx][ny] = k + 1

    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    x, y = exit_coord
    k = int(grid[x][y])
    path = [(x, y)]

    while grid[x][y] != 1:
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        found = False

        for nx, ny in neighbors:
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                if grid[nx][ny] == k - 1:
                    k -= 1
                    path.append((nx, ny))
                    x, y = nx, ny
                    found = True
                    break

        if not found:
            return None

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    x, y = coord
    rows = len(grid)
    cols = len(grid[0])

    if (x, y) in [(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)]:
        return True

    if not (x == 0 or x == rows - 1 or y == 0 or y == cols - 1):
        return False

    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < rows - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < cols - 1:
        neighbors.append((x, y + 1))

    for nx, ny in neighbors:
        if grid[nx][ny] == " ":
            return False

    return True


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[List[Tuple[int, int]]]]:
    """

    :param grid:
    :return:
    """

    grid = deepcopy(grid)
    exits = get_exits(grid)
    if len(exits) != 2:
        return grid, None

    start = exits[0]
    finish = exits[1]

    if encircled_exit(grid, start) or encircled_exit(grid, finish):
        return grid, None

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == " " or grid[x][y] == "X":
                grid[x][y] = 0

    sx, sy = start
    fx, fy = finish
    grid[sx][sy] = 1
    grid[fx][fy] = 0
    k = 1

    while grid[fx][fy] == 0:
        if not make_step(grid, k):
            return grid, None
        k += 1

    if grid[fx][fy] == 0:
        return grid, None

    path = shortest_path(grid, (fx, fy))
    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]],
    path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
