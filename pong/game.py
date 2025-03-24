# 🕹️ Pong Game

import pygame

try:
    from .game_objects import Game
except ImportError:
    from game_objects import Game


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


def main(fps: int = 60):
    clock = pygame.time.Clock()
    screen = pygame.display.get_surface()
    screen_width, screen_height = screen.get_size()
    game = Game(screen_width, screen_height)
    draw_offset_x = (screen_width - game.game_area.width) // 2
    draw_offset_y = (screen_height - game.game_area.height) // 2
    net_segment_height = game.game_area.height // 20
    net_segments = 8
    net_width = 4
    score_font = pygame.font.SysFont("comicsans", 50)
    game_over_font = pygame.font.SysFont("comicsans", 75)
    running = True

    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
        left_score_txt = score_font.render(str(game.score_left), True, WHITE)
        right_score_txt = score_font.render(str(game.score_right), True, WHITE)
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
            txt = game_over_font.render("Game Over", True, RED)
            screen.blit(txt, (screen_width // 2 - txt.get_width() // 2, screen_height // 2 - txt.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(3000)
            game.reset()

        pygame.display.update((draw_offset_x, draw_offset_y, game.game_area.width, game.game_area.height))


if __name__ == "__main__":
    TITLE = "Pong"
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    pygame.init()
    pygame.display.set_caption(TITLE)
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    main()
    pygame.quit()
