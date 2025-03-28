import pygame

try:
    from game_logic import Game
    from constants import WHITE, RED
except ImportError:
    from .game_logic import Game
    from .constants import WHITE, RED


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
    font = pygame.font.SysFont("comicsans", 50)
    left_score_txt = font.render(str(game.score_left), True, WHITE)
    right_score_txt = font.render(str(game.score_right), True, WHITE)
    screen.blit(left_score_txt, (game.game_area.width // 4 - left_score_txt.get_width() // 2 - draw_offset_x, left_score_txt.get_height() // 2 - draw_offset_y))
    screen.blit(right_score_txt, (game.game_area.width * (3 / 4) - right_score_txt.get_width() // 2 - draw_offset_x, right_score_txt.get_height() // 2 - draw_offset_y))


def draw_hits(screen: pygame.Surface, game: Game, draw_offset_x: int = 0, draw_offset_y: int = 0):
    font = pygame.font.SysFont("comicsans", 30)
    left_hits_txt = font.render(str(game.hits_left), True, RED)
    right_hits_txt = font.render(str(game.hits_right), True, RED)
    total_hits_txt = font.render(str(game.total_hits), True, RED)

    # Left hits at bottom middle left (1/4)
    screen.blit(left_hits_txt, (game.game_area.width // 4 - left_hits_txt.get_width() // 2 - draw_offset_x, game.game_area.height - left_hits_txt.get_height() - draw_offset_y))

    # Right hits at bottom middle right (3/4)
    screen.blit(right_hits_txt, (game.game_area.width * (3 / 4) - right_hits_txt.get_width() // 2 - draw_offset_x, game.game_area.height - right_hits_txt.get_height() - draw_offset_y))

    # Total hits at bottom middle (2/4)
    screen.blit(total_hits_txt, (game.game_area.width // 2 - total_hits_txt.get_width() // 2 - draw_offset_x, game.game_area.height - total_hits_txt.get_height() - draw_offset_y))
