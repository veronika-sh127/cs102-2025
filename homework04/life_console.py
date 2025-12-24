import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        rows, cols = self.life.rows, self.life.cols
        screen.border()

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        rows, cols = self.life.rows, self.life.cols

        for y in range(rows):
            for x in range(cols):
                cell = self.life.curr_generation[y][x]
                char = "O" if cell == 1 else " "
                screen.addch(y + 1, x + 1, char)

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)
        screen.nodelay(True)
        screen.keypad(True)

        try:
            while True:
                screen.clear()
                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.refresh()

                self.life.step()

                ch = screen.getch()
                if ch in (27, ord("q")):
                    break
                if self.life.is_max_generations_exceeded or not self.life.is_changing:
                    break

                curses.napms(100)
        finally:
            curses.endwin()
