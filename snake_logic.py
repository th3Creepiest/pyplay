import random
import logging
from dataclasses import dataclass
from collections import namedtuple

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
