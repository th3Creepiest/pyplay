import os
import sys
import logging
from enum import Enum, auto

import pygame
import neat

try:
    from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, RED
    from game_logic import Game
    from draw import draw_game, draw_net, draw_scores
    from ai import test_best_network
except ImportError:
    from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, RED
    from .game_logic import Game
    from .draw import draw_game, draw_net, draw_scores
    from .ai import test_best_network


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class MenuSelection(Enum):
    SINGLE_PLAYER = auto()
    MULTI_PLAYER = auto()


def main():
    logging.info("launching pong game")
    pygame.display.set_caption("Pong")
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen = pygame.display.get_surface()
    display_menu(screen)


def display_menu(screen: pygame.Surface):
    logging.info("displaying menu screen")
    screen_width, screen_height = screen.get_size()
    waiting_for_selection = True
    selection = MenuSelection.SINGLE_PLAYER

    font_100 = pygame.font.SysFont("comicsans", 100)
    font_50 = pygame.font.SysFont("comicsans", 50)
    font_28 = pygame.font.SysFont("comicsans", 28)
    font_14 = pygame.font.SysFont("comicsans", 14)

    while waiting_for_selection:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting_for_selection = False
                elif event.key == pygame.K_UP:
                    selection = MenuSelection.SINGLE_PLAYER
                elif event.key == pygame.K_DOWN:
                    selection = MenuSelection.MULTI_PLAYER
                elif event.key == pygame.K_SPACE:
                    if selection == MenuSelection.SINGLE_PLAYER:
                        run_single_player_game(screen)
                    elif selection == MenuSelection.MULTI_PLAYER:
                        run_multi_player_game(screen)

        screen.fill(BLACK)

        txt = font_100.render("PONG", True, WHITE)
        txt_rect = txt.get_rect(center=(screen_width // 2, screen_height * 0.15))
        screen.blit(txt, txt_rect)

        txt = font_50.render("Single Player", True, WHITE)
        txt_rect1 = txt.get_rect(center=(screen_width // 2, screen_height * 0.4))
        screen.blit(txt, txt_rect1)

        txt = font_50.render("Multi Player", True, WHITE)
        txt_rect2 = txt.get_rect(center=(screen_width // 2, screen_height * 0.55))
        screen.blit(txt, txt_rect2)

        txt = font_14.render("Player 1: W (up), S (down)", True, WHITE)
        txt_rect = txt.get_rect(center=(screen_width // 2, screen_height * 0.7))
        screen.blit(txt, txt_rect)

        txt = font_14.render("Player 2: Up Arrow, Down Arrow", True, WHITE)
        txt_rect = txt.get_rect(center=(screen_width // 2, screen_height * 0.75))
        screen.blit(txt, txt_rect)

        txt = font_28.render("Press SPACE to start", True, RED)
        txt_rect = txt.get_rect(center=(screen_width // 2, screen_height * 0.9))
        screen.blit(txt, txt_rect)

        flash_color = WHITE if int(pygame.time.get_ticks() / 750) % 2 == 0 else BLACK
        if selection == MenuSelection.SINGLE_PLAYER:
            pygame.draw.rect(screen, flash_color, (txt_rect1.x - 5, txt_rect1.y - 5, txt_rect1.width + 10, txt_rect1.height + 10), 2, 10)
        elif selection == MenuSelection.MULTI_PLAYER:
            pygame.draw.rect(screen, flash_color, (txt_rect2.x - 5, txt_rect2.y - 5, txt_rect2.width + 10, txt_rect2.height + 10), 2, 10)

        pygame.display.flip()


def run_single_player_game(screen: pygame.Surface):
    logging.info("single player game start")
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    test_best_network(screen, config)


def run_multi_player_game(screen: pygame.Surface):
    logging.info("multiplayer game start")

    clock = pygame.time.Clock()
    screen_width, screen_height = screen.get_size()
    game = Game(screen_width, screen_height)
    draw_offset_x = (screen_width - game.game_area.width) // 2
    draw_offset_y = (screen_height - game.game_area.height) // 2
    running = True
    fps = 60

    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            game.move_right_paddle_up()
        if keys[pygame.K_DOWN]:
            game.move_right_paddle_down()
        if keys[pygame.K_w]:
            game.move_left_paddle_up()
        if keys[pygame.K_s]:
            game.move_left_paddle_down()

        game.update()

        screen.fill(BLACK)

        draw_scores(screen, game, draw_offset_x, draw_offset_y)
        draw_net(screen, game, draw_offset_x, draw_offset_y)
        draw_game(screen, game, draw_offset_x, draw_offset_y)

        if game.game_over:
            font = pygame.font.SysFont("comicsans", 75)
            txt = font.render("Game Over", True, RED)
            txt_rect = txt.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(txt, txt_rect)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        pygame.display.update((draw_offset_x, draw_offset_y, game.game_area.width, game.game_area.height))


if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
