# 🐍 Snake Game

import sys
import random
import logging
from dataclasses import dataclass
from collections import namedtuple
import pygame

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s")


TITLE = "Snake"
GRID_CELL_SIZE = 20
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
DRAW_GRID = True

# Colors
BLACK = (0, 0, 0)
GRAY = (20, 20, 20)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


Coord = namedtuple("Coord", ["x", "y"])


@dataclass
class Grid:
    width: int
    height: int


@dataclass
class Food:
    x: int
    y: int


class Snake:

    def __init__(self, x: int, y: int, size: int = 3):
        self.positions: list[Coord] = [Coord(x - i, y) for i in range(size)]  # create initial snake segments extending to the left
        self.direction = (1, 0)  # start moving right

    def move(self):
        new_x = self.positions[0].x + self.direction[0]
        new_y = self.positions[0].y + self.direction[1]
        new_head = Coord(new_x, new_y)
        self.positions = [new_head] + self.positions[:-1]

    def change_direction(self, direction: str | int):
        if direction == "up" or direction == 0:
            new_direction = Coord(0, -1)
        elif direction == "down" or direction == 1:
            new_direction = Coord(0, 1)
        elif direction == "left" or direction == 2:
            new_direction = Coord(-1, 0)
        elif direction == "right" or direction == 3:
            new_direction = Coord(1, 0)

        opposite_dir = Coord(-self.direction[0], -self.direction[1])

        if new_direction != opposite_dir:
            self.direction = new_direction

    def eat_food(self):
        self.positions.append(self.positions[-1])


class Game:
    """Snake Game Logic"""

    def __init__(self, grid: Grid = Grid(width=150, height=150)):
        self.grid = grid
        self.start_new_game()

    def start_new_game(self):
        self.snake = Snake(self.grid.width // 2, self.grid.height // 2, size=3)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False

    def spawn_food(self):
        while True:
            x = random.randint(0, self.grid.width - 1)
            y = random.randint(0, self.grid.height - 1)
            if Coord(x, y) not in self.snake.positions:
                return Food(x, y)

    def update(self):
        self.snake.move()

        # Wrap the snake around grid boundaries
        head = self.snake.positions[0]
        new_x = head.x % self.grid.width
        new_y = head.y % self.grid.height
        self.snake.positions[0] = Coord(new_x, new_y)

        # Eat food
        if self.snake.positions[0] == Coord(self.food.x, self.food.y):
            self.snake.eat_food()
            self.food = self.spawn_food()
            self.score += 1
            logging.info(f"Snake ate food. Score: {self.score}")

        # Check for collision
        if head in self.snake.positions[1:]:
            logging.info(f"Game Over: snake collided with itself. Score: {self.score}")
            self.game_over = True


def main():

    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)

    font = pygame.font.Font(None, 50)

    while True:
        show_welcome_screen(screen, font)
        waiting_for_selection = True
        while waiting_for_selection:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        run_game(screen, font)
                        waiting_for_selection = False
                    elif event.key == pygame.K_ESCAPE:
                        quit_game()


def show_welcome_screen(screen: pygame.Surface, font: pygame.font.Font):
    screen.fill(BLACK)

    title = font.render(TITLE, True, GREEN)
    human_text = font.render("Press P for Play", True, GRAY)

    title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
    human_rect = human_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    screen.blit(title, title_rect)
    screen.blit(human_text, human_rect)

    pygame.display.flip()


def show_game_over(screen: pygame.Surface, font: pygame.font.Font, game: Game):
    game_over_text = font.render(f"Game Over! Score: {game.score}", True, RED)
    text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(game_over_text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)


def quit_game():
    pygame.quit()
    sys.exit()


def run_game(screen: pygame.Surface, font: pygame.font.Font):

    clock = pygame.time.Clock()

    game_grid = Grid(width=WINDOW_WIDTH // GRID_CELL_SIZE, height=WINDOW_HEIGHT // GRID_CELL_SIZE)

    if DRAW_GRID:
        draw_grid = [pygame.Rect(x * GRID_CELL_SIZE + 1, y * GRID_CELL_SIZE + 1, GRID_CELL_SIZE - 2, GRID_CELL_SIZE - 2) for x in range(game_grid.width) for y in range(game_grid.height)]

    game = Game(game_grid)
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_p:
                    paused = not paused
                elif not paused and event.key in [pygame.K_UP, pygame.K_w, pygame.K_k]:
                    game.snake.change_direction("up")
                elif not paused and event.key in [pygame.K_DOWN, pygame.K_s, pygame.K_j]:
                    game.snake.change_direction("down")
                elif not paused and event.key in [pygame.K_LEFT, pygame.K_a, pygame.K_h]:
                    game.snake.change_direction("left")
                elif not paused and event.key in [pygame.K_RIGHT, pygame.K_d, pygame.K_l]:
                    game.snake.change_direction("right")

        if not paused:
            game.update()

            if game.game_over:
                show_game_over(screen, font, game)
                return

        # Clear screen
        screen.fill(BLACK)

        if DRAW_GRID:
            [pygame.draw.rect(screen, GRAY, rect, width=1) for rect in draw_grid]

        # Draw the snake
        for segment in game.snake.positions:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_CELL_SIZE + 1, segment[1] * GRID_CELL_SIZE + 1, GRID_CELL_SIZE - 2, GRID_CELL_SIZE - 2))

        # Draw the food
        pygame.draw.rect(screen, RED, (game.food.x * GRID_CELL_SIZE + 1, game.food.y * GRID_CELL_SIZE + 1, GRID_CELL_SIZE - 2, GRID_CELL_SIZE - 2))

        # Update display
        pygame.display.flip()

        clock.tick(game.score + 10)


if __name__ == "__main__":
    main()
