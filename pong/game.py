import os
import sys
import logging
import pygame

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from globals import BLACK, WHITE, RED, FONT_100_CS, FONT_75_CS, FONT_50_CS, FONT_30_CS, FONT_28_CS

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
                    run_multiplayer_game(screen)

        screen.fill(BLACK)

        title_text = FONT_100_CS.render("PONG", True, WHITE)
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 5))
        screen.blit(title_text, title_rect)

        text_surface = FONT_50_CS.render("Multiplayer", True, WHITE)
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
        screen.blit(text_surface, text_rect)

        text_surface1 = FONT_28_CS.render("Player 1: W (up), S (down)", True, WHITE)
        text_rect1 = text_surface1.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text_surface1, text_rect1)

        text_surface2 = FONT_28_CS.render("Player 2: Up Arrow, Down Arrow", True, WHITE)
        text_rect2 = text_surface2.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
        screen.blit(text_surface2, text_rect2)

        text_surface3 = FONT_28_CS.render("Press SPACE to start", True, WHITE)
        text_rect3 = text_surface3.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 150))
        border_rect = pygame.Rect(text_rect3.left - 10, text_rect3.top, text_rect3.width + 20, text_rect3.height)
        flash_color = WHITE if int(pygame.time.get_ticks() / 500) % 2 == 0 else BLACK
        pygame.draw.rect(screen, flash_color, border_rect, 2)

        screen.blit(text_surface3, text_rect3)

        pygame.display.flip()


def run_multiplayer_game(screen: pygame.Surface):
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

        if game.GAME_OVER:
            txt = FONT_75_CS.render("Game Over", True, RED)
            txt_rect = txt.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(txt, txt_rect)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        pygame.display.update((draw_offset_x, draw_offset_y, game.game_area.width, game.game_area.height))


def draw_game(screen: pygame.Surface, game: Game, draw_offset_x: int = 0, draw_offset_y: int = 0):
    pygame.draw.rect(screen, WHITE, (draw_offset_x, draw_offset_y, game.game_area.width, game.game_area.height), width=1)
    pygame.draw.rect(screen, WHITE, (game.paddleR.x + draw_offset_x, game.paddleR.y + draw_offset_y, game.paddleR.width, game.paddleR.height))
    pygame.draw.rect(screen, WHITE, (game.paddleL.x + draw_offset_x, game.paddleL.y + draw_offset_y, game.paddleL.width, game.paddleL.height))
    pygame.draw.ellipse(screen, WHITE, (game.ball.x - game.ball.radius + draw_offset_x, game.ball.y - game.ball.radius + draw_offset_y, game.ball.radius * 2, game.ball.radius * 2))


def draw_net(screen: pygame.Surface, game: Game, draw_offset_x: int = 0, draw_offset_y: int = 0):
    net_width = 4
    net_segments = 8
    margin = 50
    net_segment_height = game.game_area.height // 20
    step_size = (game.game_area.height - 2 * margin) // net_segments

    for i in range(net_segments):
        y = draw_offset_y + margin + (margin / 2 - net_segment_height / 4) + i * step_size
        pygame.draw.rect(screen, WHITE, ((draw_offset_x - net_width // 2) + game.game_area.width // 2, y, net_width, net_segment_height))


def draw_scores(screen: pygame.Surface, game: Game, draw_offset_x: int = 0, draw_offset_y: int = 0):
    left_score_txt = FONT_50_CS.render(str(game.score_left), True, WHITE)
    right_score_txt = FONT_50_CS.render(str(game.score_right), True, WHITE)
    screen.blit(left_score_txt, (game.game_area.width // 4 - left_score_txt.get_width() // 2 - draw_offset_x, left_score_txt.get_height() // 2 - draw_offset_y))
    screen.blit(right_score_txt, (game.game_area.width * (3 / 4) - right_score_txt.get_width() // 2 - draw_offset_x, right_score_txt.get_height() // 2 - draw_offset_y))


def draw_hits(screen: pygame.Surface, game: Game, draw_offset_x: int = 0, draw_offset_y: int = 0):
    left_hits_txt = FONT_30_CS.render(str(game.hits_left), True, RED)
    right_hits_txt = FONT_30_CS.render(str(game.hits_right), True, RED)
    total_hits_txt = FONT_30_CS.render(str(game.hits_left + game.hits_right), True, RED)

    # Left hits at bottom middle left (1/4)
    screen.blit(left_hits_txt, (game.game_area.width // 4 - left_hits_txt.get_width() // 2 - draw_offset_x, game.game_area.height - left_hits_txt.get_height() - draw_offset_y))

    # Right hits at bottom middle right (3/4)
    screen.blit(right_hits_txt, (game.game_area.width * (3 / 4) - right_hits_txt.get_width() // 2 - draw_offset_x, game.game_area.height - right_hits_txt.get_height() - draw_offset_y))

    # Total hits at bottom middle (2/4)
    screen.blit(total_hits_txt, (game.game_area.width // 2 - total_hits_txt.get_width() // 2 - draw_offset_x, game.game_area.height - total_hits_txt.get_height() - draw_offset_y))


if __name__ == "__main__":
    TITLE = "Pong"
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    pygame.display.set_caption(TITLE)
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    main()
    pygame.quit()
