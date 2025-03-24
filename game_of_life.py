"""🌱 Conway's Game of Life

The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, live or dead.
Every cell interacts with its eight neighbors, which are the cells that are horizontally, vertically, or diagonally adjacent.

At each step in time, the following transitions occur:
1. Any live cell with fewer than two live neighbors dies, as if by under population.
2. Any live cell with two or three live neighbors lives on to the next generation.
3. Any live cell with more than three live neighbors dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

The initial pattern constitutes the seed of the system.
The first generation is created by applying the above rules simultaneously to every cell in the seed, live or dead; births and deaths occur simultaneously, and the discrete moment at which this happens is sometimes called a tick.
Each generation is a pure function of the preceding one. The rules continue to be applied repeatedly to create further generations.
"""

import sys
import pygame
import numpy as np
from constants import BLACK, WHITE


TITLE = "Conway's Game of Life"
FPS = 10
CELL_SIZE = 5
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600


def update(grid: np.ndarray) -> np.ndarray:
    rows, cols = grid.shape
    new_grid = grid.copy()

    # Iterate over every cell
    for i in range(rows):
        for j in range(cols):
            live_neighbors = 0

            # Check all neighbors in a 3x3 block
            for x in range(max(0, i - 1), min(rows, i + 2)):
                for y in range(max(0, j - 1), min(cols, j + 2)):
                    if (x, y) != (i, j):
                        live_neighbors += grid[x, y]

            # Apply Conway's rules
            if grid[i, j] == 1:
                if live_neighbors < 2 or live_neighbors > 3:
                    new_grid[i, j] = 0  # dies
            else:
                if live_neighbors == 3:
                    new_grid[i, j] = 1  # becomes alive

    return new_grid


def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)

    grid_width = WINDOW_WIDTH // CELL_SIZE
    grid_height = WINDOW_HEIGHT // CELL_SIZE
    grid = np.random.randint(2, size=(grid_height, grid_width))

    running = True
    pause = False
    iteration = 0

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE or event.key == pygame.K_p:
                    pause = not pause

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                j = pos[0] // CELL_SIZE
                i = pos[1] // CELL_SIZE
                grid[i, j] = 1 - grid[i, j]

        if not pause:
            grid = update(grid)
            iteration += 1

        screen.fill(BLACK)

        # Draw live cells
        for i in range(grid_height):
            for j in range(grid_width):
                if grid[i, j] == 1:
                    rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, WHITE, rect)

        # Render labels
        text_iteration = font.render(f"Iteration: {iteration}", True, WHITE)
        text_alive = font.render(f"Alive: {np.sum(grid)}", True, WHITE)
        screen.blit(text_iteration, (10, 10))
        screen.blit(text_alive, (10, 35))

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption(TITLE)
    main()
    pygame.quit()
    sys.exit()
