# 🐍 Snake Game

import sys
import logging
import pygame

from snake_logic import Game, Grid
from snake_ai import SnakeAI
from constants import BLACK, GRAY, GREEN, RED

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s")


TITLE = "Snake"
GRID_CELL_SIZE = 20
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
DRAW_GRID = False


def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    font = pygame.font.Font(None, 50)
    clock = pygame.time.Clock()

    game_grid = Grid(width=WINDOW_WIDTH // GRID_CELL_SIZE, height=WINDOW_HEIGHT // GRID_CELL_SIZE)

    draw_grid = None
    if DRAW_GRID:
        draw_grid = [pygame.Rect(x * GRID_CELL_SIZE + 1, y * GRID_CELL_SIZE + 1, GRID_CELL_SIZE - 2, GRID_CELL_SIZE - 2) for x in range(game_grid.width) for y in range(game_grid.height)]

    while True:
        show_welcome_screen(screen, font)
        waiting_for_selection = True
        while waiting_for_selection:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_a:
                        run_ai_game(screen, clock, game_grid, draw_grid)
                        waiting_for_selection = False
                    elif event.key == pygame.K_h:
                        run_human_game(screen, clock, font, game_grid, draw_grid)
                        waiting_for_selection = False


def show_welcome_screen(screen: pygame.Surface, font: pygame.font.Font):
    screen.fill(BLACK)

    title = font.render(TITLE, True, GREEN)
    human_text = font.render("Press H for Human Player", True, GRAY)
    ai_text = font.render("Press A for AI Player", True, GRAY)

    title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
    human_rect = human_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    ai_rect = ai_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

    screen.blit(title, title_rect)
    screen.blit(human_text, human_rect)
    screen.blit(ai_text, ai_rect)

    pygame.display.flip()


def show_game_over(screen: pygame.Surface, font: pygame.font.Font, game: Game):
    game_over_text = font.render(f"Game Over! Score: {game.score}", True, RED)
    text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(game_over_text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)


def draw_game_state(screen: pygame.Surface, game: Game, draw_grid: list[pygame.Rect]):

    # Clear the screen
    screen.fill(BLACK)

    if DRAW_GRID:
        [pygame.draw.rect(screen, GRAY, rect, width=1) for rect in draw_grid]

    # Draw the snake
    for segment in game.snake.positions:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_CELL_SIZE + 1, segment[1] * GRID_CELL_SIZE + 1, GRID_CELL_SIZE - 2, GRID_CELL_SIZE - 2))

    # Draw the food
    pygame.draw.rect(screen, RED, (game.food.x * GRID_CELL_SIZE + 1, game.food.y * GRID_CELL_SIZE + 1, GRID_CELL_SIZE - 2, GRID_CELL_SIZE - 2))

    # Update the display
    pygame.display.flip()


def run_human_game(screen: pygame.Surface, clock: pygame.time.Clock, font: pygame.font.Font, game_grid: Grid, draw_grid: list[pygame.Rect]):
    game = Game(game_grid)
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_h:
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

        draw_game_state(screen, game, draw_grid)

        clock.tick(game.score + 10)


def run_ai_game(screen: pygame.Surface, clock: pygame.time.Clock, game_grid: Grid, draw_grid: list[pygame.Rect], fps: int = 120):
    ai = SnakeAI(game_grid)
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_ESCAPE:
                    return

        if not paused:
            ai.update()

        draw_game_state(screen, ai.game, draw_grid)

        clock.tick(fps)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption(TITLE)
    main()
    pygame.quit()
    sys.exit()
