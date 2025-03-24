# 🕹️ Pong Game

import os
import sys
import logging
import pygame

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from globals import BLACK, WHITE, RED, FONT_100_CS, FONT_75_CS, FONT_50_CS, FONT_40_CS

try:
    from logic import Game
except ImportError:
    from .logic import Game


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main():
    logging.info("launching pong game")
    screen = pygame.display.get_surface()
    display_welcome_screen(screen)


def display_welcome_screen(screen: pygame.Surface):
    logging.info("displaying welcome screen")

    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting_for_start = False
                elif event.key == pygame.K_SPACE:
                    run_game(screen)

        screen.fill(BLACK)

        title_text = FONT_100_CS.render("PONG", True, WHITE)
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
        screen.blit(title_text, title_rect)

        instructions = ["Player 1: W (up), S (down)", "Player 2: Up Arrow, Down Arrow", "Press SPACE to start"]
        for i, text in enumerate(instructions):
            text_surface = FONT_40_CS.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + i * 50))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()


def run_game(screen: pygame.Surface):
    logging.info("game start")

    clock = pygame.time.Clock()
    screen_width, screen_height = screen.get_size()
    game = Game(screen_width, screen_height)
    draw_offset_x = (screen_width - game.game_area.width) // 2
    draw_offset_y = (screen_height - game.game_area.height) // 2
    net_segment_height = game.game_area.height // 20
    net_segments = 8
    net_width = 4
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

        # draw the scores
        left_score_txt = FONT_50_CS.render(str(game.score_left), True, WHITE)
        right_score_txt = FONT_50_CS.render(str(game.score_right), True, WHITE)
        screen.blit(left_score_txt, (game.game_area.width // 4 - left_score_txt.get_width() // 2 - draw_offset_x, left_score_txt.get_height() // 2 - draw_offset_y))
        screen.blit(right_score_txt, (game.game_area.width * (3 / 4) - right_score_txt.get_width() // 2 - draw_offset_x, right_score_txt.get_height() // 2 - draw_offset_y))

        # draw the net
        for y in range(draw_offset_y + 20, draw_offset_y + game.game_area.height, game.game_area.height // net_segments):
            pygame.draw.rect(screen, WHITE, ((draw_offset_x - net_width // 2) + game.game_area.width // 2, y, net_width, net_segment_height))

        pygame.draw.rect(screen, WHITE, (draw_offset_x, draw_offset_y, game.game_area.width, game.game_area.height), width=1)
        pygame.draw.rect(screen, WHITE, (game.paddleR.x + draw_offset_x, game.paddleR.y + draw_offset_y, game.paddleR.width, game.paddleR.height))
        pygame.draw.rect(screen, WHITE, (game.paddleL.x + draw_offset_x, game.paddleL.y + draw_offset_y, game.paddleL.width, game.paddleL.height))
        pygame.draw.ellipse(screen, WHITE, (game.ball.x - game.ball.radius + draw_offset_x, game.ball.y - game.ball.radius + draw_offset_y, game.ball.radius * 2, game.ball.radius * 2))

        if game.GAME_OVER:
            txt = FONT_75_CS.render("Game Over", True, RED)
            txt_rect = txt.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(txt, txt_rect)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        pygame.display.update((draw_offset_x, draw_offset_y, game.game_area.width, game.game_area.height))


if __name__ == "__main__":
    TITLE = "Pong"
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    pygame.display.set_caption(TITLE)
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    main()
    pygame.quit()
