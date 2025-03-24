import sys
import pygame
import tetris
import pong
import snake_game
import game_of_life
from constants import BLACK, WHITE


WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FONT_SIZE = 40

GAMES = [
    ("Tetris", tetris.main),
    ("Pong", pong.main),
    ("Snake Game", snake_game.main),
    ("Game of Life", game_of_life.main),
]

pygame.init()
pygame.display.set_caption("PyPlay")

icon = pygame.image.load("art/icon.jpg")
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
font = pygame.font.SysFont("arial", FONT_SIZE)


def draw_text(text, x, y):
    txt_surface = font.render(text, True, WHITE)
    txt_rect = txt_surface.get_rect(center=(x, y))
    screen.blit(txt_surface, txt_rect)


selected = 0
running = True

while running:
    screen.fill(BLACK)
    draw_text("Select a game:", WINDOW_WIDTH // 2, 100)

    for i, (name, _) in enumerate(GAMES):
        color = WHITE if i == selected else (128, 128, 128)
        text_surface = font.render(f"{i+1}. {name}", True, color)
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 200 + i * 50))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected = (selected + 1) % len(GAMES)
            elif event.key == pygame.K_UP:
                selected = (selected - 1) % len(GAMES)
            elif event.key == pygame.K_RETURN:
                _, game_func = GAMES[selected]
                game_func()

pygame.quit()
sys.exit()
