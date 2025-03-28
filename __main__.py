import pygame

import flappy
import pong
import snake
import tetris
import game_of_life


TITLE = "PyPlay"


pygame.init()
pygame.display.set_caption(TITLE)
pygame.display.set_icon(pygame.image.load("art/icon.jpg"))


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (50, 50, 50)
WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
FONT_50 = pygame.font.SysFont("arial", 50)
FONT_40 = pygame.font.SysFont("arial", 40)
GAMES = [
    ("Flappy", flappy.main),
    ("Pong", pong.main),
    ("Snake", snake.main),
    ("Tetris", tetris.main),
    ("Game of Life", game_of_life.main),
]


screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
selected = 0
running = True


while running:
    clock.tick(30)

    screen.fill(BLACK)

    pygame.draw.rect(screen, GREY, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), 5)

    txt_surface = FONT_50.render("Select a Game", True, WHITE)
    txt_rect = txt_surface.get_rect(center=(WINDOW_WIDTH // 2, 100))
    screen.blit(txt_surface, txt_rect)

    for i, (name, _) in enumerate(GAMES):
        color = WHITE if i == selected else GREY
        text_surface = FONT_40.render(f"{i+1}. {name}", True, color)
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 200 + i * 50))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_DOWN:
                selected = (selected + 1) % len(GAMES)
            elif event.key == pygame.K_UP:
                selected = (selected - 1) % len(GAMES)
            elif event.key == pygame.K_1:
                selected = 0
            elif event.key == pygame.K_2:
                selected = 1
            elif event.key == pygame.K_3:
                selected = 2
            elif event.key == pygame.K_4:
                selected = 3
            elif event.key == pygame.K_5:
                selected = 4
            elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                _, game_func = GAMES[selected]
                game_func()
                screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                pygame.display.set_caption(TITLE)

pygame.quit()
