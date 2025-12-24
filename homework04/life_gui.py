import pygame
from life import GameOfLife
from pygame.locals import QUIT
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)

        self.cell_size = cell_size
        self.speed = speed
        width = self.life.cols * self.cell_size
        height = self.life.rows * self.cell_size
        self.screen_size = (width, height)
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Game of Life")

    def draw_lines(self) -> None:
        width, height = self.screen_size

        for x in range(0, width, self.cell_size):
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (x, 0),
                (x, height),
            )
        for y in range(0, height, self.cell_size):
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (0, y),
                (width, y),
            )

    def draw_grid(self) -> None:
        """Отобразить состояние клеток."""
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                cell = self.life.curr_generation[y][x]
                color = pygame.Color("green") if cell == 1 else pygame.Color("white")

                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, color, rect)

    def run(self) -> None:
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()

            self.life.step()
            if self.life.is_max_generations_exceeded or not self.life.is_changing:
                running = False

            clock.tick(self.speed)

        pygame.quit()


if __name__ == "__main__":
    life = GameOfLife((30, 60), randomize=True, max_generations=1000)
    gui_ui = GUI(life)
    gui_ui.run()
